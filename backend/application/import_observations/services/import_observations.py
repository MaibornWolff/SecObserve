import os
from dataclasses import dataclass
from typing import Optional, Tuple

from django.core.files.base import File
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Parser,
    Product,
    Reference,
    Service,
)
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
from application.core.services.potential_duplicates import find_potential_duplicates
from application.core.services.product import set_repository_default_branch
from application.core.services.security_gate import check_security_gate
from application.core.types import Status
from application.epss.services.epss import epss_apply_observation
from application.import_observations.models import (
    Api_Configuration,
    Vulnerability_Check,
)
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseFileParser,
    BaseParser,
)
from application.import_observations.services.parser_registry import get_parser_class
from application.issue_tracker.services.issue_tracker import (
    push_observations_to_issue_tracker,
)
from application.rules.services.rule_engine import Rule_Engine


@dataclass
class ImportParameters:
    product: Product
    branch: Optional[Branch]
    parser: Parser
    filename: str
    api_configuration_name: str
    service: str
    docker_image_name_tag: str
    endpoint_url: str
    imported_observations: list[Observation]


@dataclass
class FileUploadParameters:
    product: Product
    branch: Optional[Branch]
    parser: Parser
    file: File
    service: str
    docker_image_name_tag: str
    endpoint_url: str


def file_upload_observations(
    file_upload_parameters: FileUploadParameters,
) -> Tuple[int, int, int]:
    parser_instance = _instanciate_parser(file_upload_parameters.parser)

    if not isinstance(parser_instance, BaseFileParser):
        raise ParserError(f"{file_upload_parameters.parser.name} isn't a file parser")

    format_valid, errors, data = parser_instance.check_format(
        file_upload_parameters.file
    )
    if not format_valid:
        raise ValidationError("File format is not valid: " + " / ".join(errors))

    imported_observations = parser_instance.get_observations(data)

    filename = (
        os.path.basename(file_upload_parameters.file.name)
        if file_upload_parameters.file.name
        else ""
    )

    import_parameters = ImportParameters(
        product=file_upload_parameters.product,
        branch=file_upload_parameters.branch,
        parser=file_upload_parameters.parser,
        filename=filename,
        api_configuration_name="",
        service=file_upload_parameters.service,
        docker_image_name_tag=file_upload_parameters.docker_image_name_tag,
        endpoint_url=file_upload_parameters.endpoint_url,
        imported_observations=imported_observations,
    )

    numbers: Tuple[int, int, int, str] = _process_data(import_parameters)

    Vulnerability_Check.objects.update_or_create(
        product=import_parameters.product,
        branch=import_parameters.branch,
        filename=import_parameters.filename,
        defaults={
            "last_import_observations_new": numbers[0],
            "last_import_observations_updated": numbers[1],
            "last_import_observations_resolved": numbers[2],
            "scanner": numbers[3],
        },
    )

    return numbers[0], numbers[1], numbers[2]


def api_import_observations(
    api_configuration: Api_Configuration,
    branch: Optional[Branch],
    service: str,
    docker_image_name_tag: str,
    endpoint_url: str,
) -> Tuple[int, int, int]:
    parser_instance = _instanciate_parser(api_configuration.parser)

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
        branch=branch,
        parser=api_configuration.parser,
        filename="",
        api_configuration_name=api_configuration.name,
        service=service,
        docker_image_name_tag=docker_image_name_tag,
        endpoint_url=endpoint_url,
        imported_observations=imported_observations,
    )

    numbers: Tuple[int, int, int, str] = _process_data(import_parameters)

    Vulnerability_Check.objects.update_or_create(
        product=import_parameters.product,
        branch=import_parameters.branch,
        api_configuration_name=import_parameters.api_configuration_name,
        defaults={
            "last_import_observations_new": numbers[0],
            "last_import_observations_updated": numbers[1],
            "last_import_observations_resolved": numbers[2],
            "scanner": numbers[3],
        },
    )

    return numbers[0], numbers[1], numbers[2]


def api_check_connection(
    api_configuration: Api_Configuration,
) -> Tuple[bool, list[str]]:
    parser_instance = _instanciate_parser(api_configuration.parser)

    if not isinstance(parser_instance, BaseAPIParser):
        return False, [f"{api_configuration.parser.name} isn't an API parser"]

    format_valid, errors, _ = parser_instance.check_connection(api_configuration)

    return format_valid, errors


def _instanciate_parser(parser: Parser) -> BaseParser:
    parser_class = get_parser_class(parser.name)
    if not parser_class:
        raise ParserError(f"Parser {parser.name} not found in parser registry")
    parser_instance: BaseParser = parser_class()
    return parser_instance


def _process_data(import_parameters: ImportParameters) -> Tuple[int, int, int, str]:
    observations_new = 0
    observations_updated = 0

    scanner = ""

    rule_engine = Rule_Engine(product=import_parameters.product)

    # Read current observations for the same vulnerability check, to find updated and resolved observations
    observations_before: dict[str, Observation] = {}
    for observation_before_for_dict in get_observations_for_vulnerability_check(
        import_parameters.product,
        import_parameters.branch,
        import_parameters.filename,
        import_parameters.api_configuration_name,
    ):
        observations_before[observation_before_for_dict.identity_hash] = (
            observation_before_for_dict
        )
        scanner = observation_before_for_dict.scanner

    observations_this_run: set[str] = set()
    vulnerability_check_observations: set[Observation] = set()

    for imported_observation in import_parameters.imported_observations:
        # Set additional data in newly uploaded observation
        _prepare_imported_observation(
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
                _process_current_observation(imported_observation, observation_before)

                rule_engine.apply_rules_for_observation(observation_before)

                if observation_before.current_status == Status.STATUS_OPEN:
                    observations_updated += 1

                # Remove observation from list of current observations because it is still part of the check
                observations_before.pop(observation_before.identity_hash)
                # Add identity_hash to set of observations in this run to detect duplicates in this run
                observations_this_run.add(observation_before.identity_hash)
                vulnerability_check_observations.add(observation_before)
            else:
                _process_new_observation(imported_observation)

                rule_engine.apply_rules_for_observation(imported_observation)

                if imported_observation.current_status == Status.STATUS_OPEN:
                    observations_new += 1

                # Add identity_hash to set of observations in this run to detect duplicates in this run
                observations_this_run.add(imported_observation.identity_hash)
                vulnerability_check_observations.add(imported_observation)

        scanner = imported_observation.scanner

    observations_resolved = _resolve_unimported_observations(observations_before)
    vulnerability_check_observations.update(observations_resolved)
    check_security_gate(import_parameters.product)
    set_repository_default_branch(import_parameters.product)
    if import_parameters.branch:
        import_parameters.branch.last_import = timezone.now()
        import_parameters.branch.save()
    push_observations_to_issue_tracker(
        import_parameters.product, vulnerability_check_observations
    )
    find_potential_duplicates(
        import_parameters.product, import_parameters.branch, import_parameters.service
    )

    return observations_new, observations_updated, len(observations_resolved), scanner


def _prepare_imported_observation(
    import_parameters: ImportParameters, imported_observation: Observation
) -> None:
    imported_observation.product = import_parameters.product
    imported_observation.branch = import_parameters.branch
    imported_observation.parser = import_parameters.parser
    if not imported_observation.scanner:
        imported_observation.scanner = import_parameters.parser.name
    imported_observation.upload_filename = import_parameters.filename
    imported_observation.api_configuration_name = (
        import_parameters.api_configuration_name
    )
    imported_observation.import_last_seen = timezone.now()
    if import_parameters.service:
        imported_observation.origin_service_name = import_parameters.service
        service = Service.objects.get_or_create(
            product=import_parameters.product, name=import_parameters.service
        )[0]
        imported_observation.origin_service = service
    if import_parameters.docker_image_name_tag:
        imported_observation.origin_docker_image_name_tag = (
            import_parameters.docker_image_name_tag
        )
    if import_parameters.endpoint_url:
        imported_observation.origin_endpoint_url = import_parameters.endpoint_url


def _process_current_observation(
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

    observation_before.origin_component_dependencies = (
        imported_observation.origin_component_dependencies
    )

    previous_severity = observation_before.current_severity
    observation_before.parser_severity = imported_observation.parser_severity
    observation_before.current_severity = get_current_severity(observation_before)

    previous_status = observation_before.current_status
    if imported_observation.parser_status:
        observation_before.parser_status = imported_observation.parser_status
    else:
        # Reopen the current observation if it is resolved,
        # leave the status as is otherwise.
        if observation_before.parser_status == Status.STATUS_RESOLVED:
            observation_before.parser_status = Status.STATUS_OPEN
    observation_before.current_status = get_current_status(observation_before)

    epss_apply_observation(observation_before)
    observation_before.import_last_seen = timezone.now()
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


def _process_new_observation(imported_observation: Observation) -> None:
    imported_observation.current_severity = get_current_severity(imported_observation)

    if not imported_observation.parser_status:
        imported_observation.parser_status = Status.STATUS_OPEN
    imported_observation.current_status = get_current_status(imported_observation)

    # Observation has not been imported before, so it is a new one
    epss_apply_observation(imported_observation)
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


def _resolve_unimported_observations(
    observations_before: dict[str, Observation]
) -> set[Observation]:
    # All observations that are still in observations_before are not in the imported scan
    # and seem to have been resolved.
    observations_resolved: set[Observation] = set()
    for observation in observations_before.values():
        old_status = get_current_status(observation)

        observation.parser_status = Status.STATUS_RESOLVED
        observation.save()

        new_status = get_current_status(observation)
        if old_status != new_status:
            if old_status == Status.STATUS_OPEN:
                observations_resolved.add(observation)

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
