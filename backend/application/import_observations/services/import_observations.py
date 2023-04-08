from datetime import datetime
from typing import Tuple, Optional
from django.core.files.base import File
from django.utils.timezone import make_aware
from rest_framework.exceptions import ValidationError

from application.core.models import (
    Observation,
    Product,
    Reference,
    Parser,
    Evidence,
)
from application.core.queries.observation import (
    get_observations_for_vulnerability_check,
)
from application.core.services.observation import (
    get_identity_hash,
    get_current_severity,
    get_current_status,
    normalize_observation_fields,
    clip_fields,
)
from application.core.services.observation_log import create_observation_log
from application.core.services.security_gate import check_security_gate
from application.import_observations.models import Api_Configuration
from application.import_observations.services.parser_registry import get_parser_class
from application.import_observations.parsers.base_parser import (
    BaseParser,
    BaseAPIParser,
    BaseFileParser,
)
from application.rules.services.rule_engine import Rule_Engine


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
        raise Exception(f"{parser.name} isn't a file parser")

    format_valid, errors, data = parser_instance.check_format(file)
    if not format_valid:
        raise ValidationError("File format is not valid: " + " / ".join(errors))

    imported_observations = parser_instance.get_observations(data)

    return process_data(
        product,
        parser,
        file.name,  # type: ignore[arg-type]
        "",
        service,
        docker_image_name_tag,
        endpoint_url,
        imported_observations,
    )


def api_import_observations(
    api_configuration: Api_Configuration,
    service: str,
    docker_image_name_tag: str,
    endpoint_url: str,
) -> Tuple[int, int, int]:
    parser_instance = instanciate_parser(api_configuration.parser)

    if not isinstance(parser_instance, BaseAPIParser):
        raise Exception(f"{api_configuration.parser.name} isn't an API parser")

    format_valid, errors, data = parser_instance.check_connection(api_configuration)
    if not format_valid:
        raise ValidationError(
            "Connection couldn't be established: " + " / ".join(errors)
        )

    imported_observations = parser_instance.get_observations(data)

    return process_data(
        api_configuration.product,
        api_configuration.parser,
        "",
        api_configuration.name,
        service,
        docker_image_name_tag,
        endpoint_url,
        imported_observations,
    )


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
        raise Exception(f"Parser {parser.name} not found in parser registry")
    parser_instance: BaseParser = parser_class()
    return parser_instance


def process_data(
    product: Product,
    parser: Parser,
    filename: str,
    api_configuration_name: str,
    service: str,
    docker_image_name_tag: str,
    endpoint_url: str,
    imported_observations: list[Observation],
) -> Tuple[int, int, int]:
    observations_new = 0
    observations_updated = 0
    observations_resolved = 0

    rule_engine = Rule_Engine(product=product, parser=parser)

    # Read current observations for the same vulnerability check, to find updated and resolved observations
    observations_before: dict[str, Observation] = {}
    observations_before_list = get_observations_for_vulnerability_check(
        product, parser, filename, api_configuration_name
    )

    for observation_before_for_dict in observations_before_list:
        observations_before[
            observation_before_for_dict.identity_hash
        ] = observation_before_for_dict

    observations_this_run: set[str] = set()

    for imported_observation in imported_observations:
        # Set additional data in newly uploaded observation
        imported_observation.product = product
        imported_observation.parser = parser
        if not imported_observation.scanner:
            imported_observation.scanner = parser.name
        imported_observation.upload_filename = filename
        imported_observation.api_configuration_name = api_configuration_name
        imported_observation.import_last_seen = make_aware(datetime.now())
        if service:
            imported_observation.origin_service_name = service
        if docker_image_name_tag:
            imported_observation.origin_docker_image_name_tag = docker_image_name_tag
        if endpoint_url:
            imported_observation.origin_endpoint_url = endpoint_url
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
                observations_updated += 1

                # Set data in the current observation from the new observation
                observation_before.title = imported_observation.title
                observation_before.description = imported_observation.description
                observation_before.recommendation = imported_observation.recommendation
                observation_before.scanner_observation_id = (
                    imported_observation.scanner_observation_id
                )
                observation_before.vulnerability_id = (
                    imported_observation.vulnerability_id
                )
                observation_before.cvss3_score = imported_observation.cvss3_score
                observation_before.cvss3_vector = imported_observation.cvss3_vector
                observation_before.cwe = imported_observation.cwe
                observation_before.found = imported_observation.found
                observation_before.scanner = imported_observation.scanner

                previous_severity = observation_before.current_severity
                observation_before.parser_severity = (
                    imported_observation.parser_severity
                )
                observation_before.current_severity = get_current_severity(
                    observation_before
                )

                previous_status = observation_before.current_status
                if imported_observation.parser_status:
                    observation_before.parser_status = (
                        imported_observation.parser_status
                    )
                else:
                    # Reopen the current observation if it is resolved,
                    # leave the status as is otherwise.
                    if observation_before.parser_status == Observation.STATUS_RESOLVED:
                        observation_before.parser_status = Observation.STATUS_OPEN
                observation_before.current_status = get_current_status(
                    observation_before
                )

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

                rule_engine.apply_rules_for_observation(observation_before)

                # Remove observation from list of current observations because it is still part of the check
                observations_before.pop(observation_before.identity_hash)

                # Add identity_hash to set of observations in this run to detect duplicates in this run
                observations_this_run.add(observation_before.identity_hash)
            else:
                observations_new += 1

                imported_observation.current_severity = get_current_severity(
                    imported_observation
                )

                if not imported_observation.parser_status:
                    imported_observation.parser_status = Observation.STATUS_OPEN
                imported_observation.current_status = get_current_status(
                    imported_observation
                )

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
                rule_engine.apply_rules_for_observation(imported_observation)

                # Add identity_hash to set of observations in this run to detect duplicates in this run
                observations_this_run.add(imported_observation.identity_hash)

    # All observations that are still in observations_before are not in the imported scan
    # and seem to have been resolved.
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

    check_security_gate(product)
    return observations_new, observations_updated, observations_resolved
