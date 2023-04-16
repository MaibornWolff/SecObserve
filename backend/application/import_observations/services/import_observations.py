from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from django.core.files.base import File
from django.utils.timezone import make_aware
from rest_framework.exceptions import ValidationError

from application.core.models import Evidence, Observation, Parser, Product, Reference
from application.core.queries.observation import (
    get_observations_for_vulnerability_check,
)
from application.core.services.observation import (
    clip_fields,
    get_current_severity,
    get_current_status,
    get_identity_hash,
    normalize_observation_fields,
)
from application.core.services.observation_log import create_observation_log
from application.core.services.security_gate import check_security_gate
from application.import_observations.models import Api_Configuration
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseFileParser,
    BaseParser,
)
from application.import_observations.services.parser_registry import get_parser_class
from application.rules.services.rule_engine import Rule_Engine


@dataclass
class ImportParameters:
    product: Product
    parser: Parser
    filename: str
    api_configuration_name: str
    service: str
    docker_image_name_tag: str
    endpoint_url: str
    imported_observations: list[Observation]


def file_upload_observations(
    product: Product,
    parser: Parser,
    file: File,
    service: str,
    docker_image_name_tag: str,
    endpoint_url: str,
) -> Tuple[int, int, int]:
    parser_instance = instanciate_parser(parser)

    if not isinstance(parser_instance, BaseFileParser):
        raise ParserError(f"{parser.name} isn't a file parser")

    format_valid, errors, data = parser_instance.check_format(file)
    if not format_valid:
        raise ValidationError("File format is not valid: " + " / ".join(errors))

    imported_observations = parser_instance.get_observations(data)

    filename = file.name if file.name else ""

    import_parameters = ImportParameters(
        product=product,
        parser=parser,
        filename=filename,
        api_configuration_name="",
        service=service,
        docker_image_name_tag=docker_image_name_tag,
        endpoint_url=endpoint_url,
        imported_observations=imported_observations,
    )

    return process_data(import_parameters)


def api_import_observations(
    api_configuration: Api_Configuration,
    service: str,
    docker_image_name_tag: str,
    endpoint_url: str,
) -> Tuple[int, int, int]:
    parser_instance = instanciate_parser(api_configuration.parser)

    if not isinstance(parser_instance, BaseAPIParser):
        raise ParserError(f"{api_configuration.parser.name} isn't an API parser")

    format_valid, errors, data = parser_instance.check_connection(api_configuration)
    if not format_valid:
        raise ValidationError(
            "Connection couldn't be established: " + " / ".join(errors)
        )

    imported_observations = parser_instance.get_observations(data)

    import_parameters = ImportParameters(
        product=api_configuration.product,
        parser=api_configuration.parser,
        filename="",
        api_configuration_name=api_configuration.name,
        service=service,
        docker_image_name_tag=docker_image_name_tag,
        endpoint_url=endpoint_url,
        imported_observations=imported_observations,
    )

    return process_data(import_parameters)


def api_check_connection(
    api_configuration: Api_Configuration,
) -> Tuple[bool, list[str]]:
    parser_instance = instanciate_parser(api_configuration.parser)

    if not isinstance(parser_instance, BaseAPIParser):
        return False, [f"{api_configuration.parser.name} isn't an API parser"]

    format_valid, errors, _ = parser_instance.check_connection(api_configuration)

    return format_valid, errors


def instanciate_parser(parser: Parser) -> BaseParser:
    parser_class = get_parser_class(parser.name)
    if not parser_class:
        raise ParserError(f"Parser {parser.name} not found in parser registry")
    parser_instance: BaseParser = parser_class()
    return parser_instance


def process_data(import_parameters: ImportParameters) -> Tuple[int, int, int]:
    observations_new = 0
    observations_updated = 0

    rule_engine = Rule_Engine(
        product=import_parameters.product, parser=import_parameters.parser
    )

    # Read current observations for the same vulnerability check, to find updated and resolved observations
    observations_before: dict[str, Observation] = {}
    for observation_before_for_dict in get_observations_for_vulnerability_check(
        import_parameters.product,
        import_parameters.parser,
        import_parameters.filename,
        import_parameters.api_configuration_name,
    ):
        observations_before[
            observation_before_for_dict.identity_hash
        ] = observation_before_for_dict

    observations_this_run: set[str] = set()

    for imported_observation in import_parameters.imported_observations:
        # Set additional data in newly uploaded observation
        prepare_imported_observation(
            import_parameters,
            imported_observation,
        )
        normalize_observation_fields(imported_observation)
        clip_fields("Observation", imported_observation)
        imported_observation.identity_hash = get_identity_hash(imported_observation)

        # Only process observation if it hasn't been processed in this run before
        if imported_observation.identity_hash not in observations_this_run:
            # Check if new observation is already there in the same check
            observation_before = observations_before.get(
                imported_observation.identity_hash
            )
            if observation_before:
                process_current_observation(imported_observation, observation_before)

                observations_updated += 1
                rule_engine.apply_rules_for_observation(observation_before)
                # Remove observation from list of current observations because it is still part of the check
                observations_before.pop(observation_before.identity_hash)
                # Add identity_hash to set of observations in this run to detect duplicates in this run
                observations_this_run.add(observation_before.identity_hash)
            else:
                process_new_observation(imported_observation)

                observations_new += 1
                rule_engine.apply_rules_for_observation(imported_observation)
                # Add identity_hash to set of observations in this run to detect duplicates in this run
                observations_this_run.add(imported_observation.identity_hash)

    observations_resolved = resolve_unimported_observations(observations_before)
    check_security_gate(import_parameters.product)

    return observations_new, observations_updated, observations_resolved


def prepare_imported_observation(
    import_parameters: ImportParameters, imported_observation: Observation
) -> None:
    imported_observation.product = import_parameters.product
    imported_observation.parser = import_parameters.parser
    if not imported_observation.scanner:
        imported_observation.scanner = import_parameters.parser.name
    imported_observation.upload_filename = import_parameters.filename
    imported_observation.api_configuration_name = (
        import_parameters.api_configuration_name
    )
    imported_observation.import_last_seen = make_aware(datetime.now())
    if import_parameters.service:
        imported_observation.origin_service_name = import_parameters.service
    if import_parameters.docker_image_name_tag:
        imported_observation.origin_docker_image_name_tag = (
            import_parameters.docker_image_name_tag
        )
    if import_parameters.endpoint_url:
        imported_observation.origin_endpoint_url = import_parameters.endpoint_url


def process_current_observation(
    imported_observation: Observation, observation_before: Observation
) -> None:
    # Set data in the current observation from the new observation
    observation_before.title = imported_observation.title
    observation_before.description = imported_observation.description
    observation_before.recommendation = imported_observation.recommendation
    observation_before.scanner_observation_id = (
        imported_observation.scanner_observation_id
    )
    observation_before.vulnerability_id = imported_observation.vulnerability_id
    observation_before.cvss3_score = imported_observation.cvss3_score
    observation_before.cvss3_vector = imported_observation.cvss3_vector
    observation_before.cwe = imported_observation.cwe
    observation_before.found = imported_observation.found
    observation_before.scanner = imported_observation.scanner

    previous_severity = observation_before.current_severity
    observation_before.parser_severity = imported_observation.parser_severity
    observation_before.current_severity = get_current_severity(observation_before)

    previous_status = observation_before.current_status
    if imported_observation.parser_status:
        observation_before.parser_status = imported_observation.parser_status
    else:
        # Reopen the current observation if it is resolved,
        # leave the status as is otherwise.
        if observation_before.parser_status == Observation.STATUS_RESOLVED:
            observation_before.parser_status = Observation.STATUS_OPEN
    observation_before.current_status = get_current_status(observation_before)

    observation_before.import_last_seen = make_aware(datetime.now())
    observation_before.save()

    observation_before.references.all().delete()
    if imported_observation.unsaved_references:
        for reference in imported_observation.unsaved_references:
            reference = Reference(
                observation=observation_before,
                url=reference,
            )
            clip_fields("Reference", reference)
            reference.save()

    observation_before.evidences.all().delete()
    if imported_observation.unsaved_evidences:
        for evidence in imported_observation.unsaved_evidences:
            evidence = Evidence(
                observation=observation_before,
                name=evidence[0],
                evidence=evidence[1],
            )
            clip_fields("Evidence", evidence)
            evidence.save()

            # Write observation log if status or severity has been changed
    if (
        previous_status != observation_before.current_status
        or previous_severity != observation_before.current_severity
    ):
        if previous_status != observation_before.current_status:
            status = observation_before.current_status
        else:
            status = ""
        if previous_severity != observation_before.current_severity:
            severity = imported_observation.current_severity
        else:
            severity = ""

        create_observation_log(
            observation_before, severity, status, "Updated by parser"
        )


def process_new_observation(imported_observation: Observation) -> None:
    imported_observation.current_severity = get_current_severity(imported_observation)

    if not imported_observation.parser_status:
        imported_observation.parser_status = Observation.STATUS_OPEN
    imported_observation.current_status = get_current_status(imported_observation)

    # Observation has not been imported before, so it is a new one
    imported_observation.save()

    if imported_observation.unsaved_references:
        for reference in imported_observation.unsaved_references:
            reference = Reference(
                observation=imported_observation,
                url=reference,
            )
            clip_fields("Reference", reference)
            reference.save()

    if imported_observation.unsaved_evidences:
        for evidence in imported_observation.unsaved_evidences:
            evidence = Evidence(
                observation=imported_observation,
                name=evidence[0],
                evidence=evidence[1],
            )
            clip_fields("Evidence", evidence)
            evidence.save()

    create_observation_log(
        imported_observation,
        imported_observation.current_severity,
        imported_observation.current_status,
        "Set by parser",
    )


def resolve_unimported_observations(observations_before: dict[str, Observation]) -> int:
    # All observations that are still in observations_before are not in the imported scan
    # and seem to have been resolved.
    observations_resolved = 0
    for observation in observations_before.values():
        observation.parser_status = Observation.STATUS_RESOLVED
        observation.save()
        new_status = get_current_status(observation)
        if observation.current_status != new_status:
            observations_resolved += 1

            observation.current_status = new_status
            create_observation_log(
                observation,
                "",
                observation.current_status,
                "Observation not found in latest scan",
            )

    return observations_resolved


class ParserError(Exception):
    def __init__(self, message):
        self.message = message
