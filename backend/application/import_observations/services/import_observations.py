import os
from dataclasses import dataclass
from typing import Optional, Tuple

from django.core.files.base import File
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.commons.models import Settings
from application.commons.services.functions import clip_fields
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Product,
    Reference,
    Service,
)
from application.core.queries.observation import (
    get_observations_for_vulnerability_check,
)
from application.core.services.observation import (
    get_current_severity,
    get_current_status,
    get_identity_hash,
    normalize_observation_fields,
)
from application.core.services.observation_log import create_observation_log
from application.core.services.potential_duplicates import find_potential_duplicates
from application.core.services.product import set_repository_default_branch
from application.core.services.risk_acceptance_expiry import (
    calculate_risk_acceptance_expiry_date,
)
from application.core.services.security_gate import check_security_gate
from application.core.types import Assessment_Status, Status
from application.epss.services.cvss_bt import apply_exploit_information
from application.epss.services.epss import apply_epss
from application.import_observations.exceptions import ParserError
from application.import_observations.models import (
    Api_Configuration,
    Parser,
    Vulnerability_Check,
)
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseFileParser,
)
from application.import_observations.services.parser_detector import (
    detect_parser,
    instanciate_parser,
)
from application.issue_tracker.services.issue_tracker import (
    push_observations_to_issue_tracker,
)
from application.licenses.services.license_component import process_license_components
from application.rules.services.rule_engine import Rule_Engine
from application.vex.services.vex_engine import VEX_Engine


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
    kubernetes_cluster: str
    imported_observations: list[Observation]


@dataclass
class FileUploadParameters:
    product: Product
    branch: Optional[Branch]
    file: File
    service: str
    docker_image_name_tag: str
    endpoint_url: str
    kubernetes_cluster: str
    suppress_licenses: bool
    sbom: bool


@dataclass
class ApiImportParameters:
    api_configuration: Api_Configuration
    branch: Optional[Branch]
    service: str
    docker_image_name_tag: str
    endpoint_url: str
    kubernetes_cluster: str


def file_upload_observations(
    file_upload_parameters: FileUploadParameters,
) -> Tuple[int, int, int, int, int, int]:

    settings = Settings.load()
    parser, parser_instance, data = detect_parser(file_upload_parameters.file)
    filename = os.path.basename(file_upload_parameters.file.name) if file_upload_parameters.file.name else ""

    numbers_observations: Tuple[int, int, int, str] = 0, 0, 0, ""
    new_observations = None
    updated_observations = None
    resolved_observations = None

    if not file_upload_parameters.sbom:
        imported_observations = parser_instance.get_observations(
            data, file_upload_parameters.product, file_upload_parameters.branch
        )

        import_parameters = ImportParameters(
            product=file_upload_parameters.product,
            branch=file_upload_parameters.branch,
            parser=parser,
            filename=filename,
            api_configuration_name="",
            service=file_upload_parameters.service,
            docker_image_name_tag=file_upload_parameters.docker_image_name_tag,
            endpoint_url=file_upload_parameters.endpoint_url,
            kubernetes_cluster=file_upload_parameters.kubernetes_cluster,
            imported_observations=imported_observations,
        )

        numbers_observations = _process_data(import_parameters, settings)
        new_observations = numbers_observations[0]
        updated_observations = numbers_observations[1]
        resolved_observations = numbers_observations[2]
    else:
        if not isinstance(parser_instance, BaseFileParser) or not parser_instance.sbom():
            raise ValidationError(f"{parser.name} is not a SBOM parser")

    vulnerability_check, _ = Vulnerability_Check.objects.update_or_create(
        product=file_upload_parameters.product,
        branch=file_upload_parameters.branch,
        filename=filename,
        api_configuration_name="",
        defaults={
            "last_import_observations_new": new_observations,
            "last_import_observations_updated": updated_observations,
            "last_import_observations_resolved": resolved_observations,
            "last_import_licenses_new": None,
            "last_import_licenses_updated": None,
            "last_import_licenses_deleted": None,
            "scanner": numbers_observations[3],
        },
    )

    numbers_license_components = (0, 0, 0)
    if settings.feature_license_management and (
        not file_upload_parameters.suppress_licenses or file_upload_parameters.sbom
    ):
        imported_license_components = parser_instance.get_license_components(data)
        numbers_license_components = process_license_components(imported_license_components, vulnerability_check)

    return (
        numbers_observations[0],
        numbers_observations[1],
        numbers_observations[2],
        numbers_license_components[0],
        numbers_license_components[1],
        numbers_license_components[2],
    )


def api_import_observations(
    api_import_parameters: ApiImportParameters,
) -> Tuple[int, int, int]:
    parser_instance = instanciate_parser(api_import_parameters.api_configuration.parser)

    if not isinstance(parser_instance, BaseAPIParser):
        raise ParserError(f"{api_import_parameters.api_configuration.parser.name} isn't an API parser")

    format_valid, errors, data = parser_instance.check_connection(api_import_parameters.api_configuration)
    if not format_valid:
        raise ValidationError("Connection couldn't be established: " + " / ".join(errors))

    imported_observations = parser_instance.get_observations(
        data,
        api_import_parameters.api_configuration.product,
        api_import_parameters.branch,
    )

    import_parameters = ImportParameters(
        product=api_import_parameters.api_configuration.product,
        branch=api_import_parameters.branch,
        parser=api_import_parameters.api_configuration.parser,
        filename="",
        api_configuration_name=api_import_parameters.api_configuration.name,
        service=api_import_parameters.service,
        docker_image_name_tag=api_import_parameters.docker_image_name_tag,
        endpoint_url=api_import_parameters.endpoint_url,
        kubernetes_cluster=api_import_parameters.kubernetes_cluster,
        imported_observations=imported_observations,
    )

    numbers: Tuple[int, int, int, str] = _process_data(import_parameters, Settings.load())

    Vulnerability_Check.objects.update_or_create(
        product=import_parameters.product,
        branch=import_parameters.branch,
        filename="",
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
    parser_instance = instanciate_parser(api_configuration.parser)

    if not isinstance(parser_instance, BaseAPIParser):
        return False, [f"{api_configuration.parser.name} isn't an API parser"]

    format_valid, errors, _ = parser_instance.check_connection(api_configuration)

    return format_valid, errors


def _process_data(import_parameters: ImportParameters, settings: Settings) -> Tuple[int, int, int, str]:
    observations_new = 0
    observations_updated = 0

    scanner = ""

    rule_engine = Rule_Engine(product=import_parameters.product)
    vex_engine = VEX_Engine(import_parameters.product, import_parameters.branch)

    # Read current observations for the same vulnerability check, to find updated and resolved observations
    observations_before: dict[str, Observation] = {}
    for observation_before_for_dict in get_observations_for_vulnerability_check(
        import_parameters.product,
        import_parameters.branch,
        import_parameters.filename,
        import_parameters.api_configuration_name,
    ):
        observations_before[observation_before_for_dict.identity_hash] = observation_before_for_dict
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
        clip_fields("core", "Observation", imported_observation)
        imported_observation.identity_hash = get_identity_hash(imported_observation)

        # Only process observation if it hasn't been processed in this run before
        if imported_observation.identity_hash not in observations_this_run:
            # Check if new observation is already there in the same check
            observation_before = observations_before.get(imported_observation.identity_hash)
            if observation_before:
                _process_current_observation(imported_observation, observation_before, settings)

                rule_engine.apply_rules_for_observation(observation_before)
                vex_engine.apply_vex_statements_for_observation(observation_before)

                if observation_before.current_status == _get_initial_status(observation_before.product):
                    observations_updated += 1

                # Remove observation from list of current observations because it is still part of the check
                observations_before.pop(observation_before.identity_hash)
                # Add identity_hash to set of observations in this run to detect duplicates in this run
                observations_this_run.add(observation_before.identity_hash)
                vulnerability_check_observations.add(observation_before)
            else:
                _process_new_observation(imported_observation, settings)

                rule_engine.apply_rules_for_observation(imported_observation)
                vex_engine.apply_vex_statements_for_observation(imported_observation)

                if imported_observation.current_status == _get_initial_status(imported_observation.product):
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
    push_observations_to_issue_tracker(import_parameters.product, vulnerability_check_observations)
    find_potential_duplicates(import_parameters.product, import_parameters.branch, import_parameters.service)

    return observations_new, observations_updated, len(observations_resolved), scanner


def _prepare_imported_observation(import_parameters: ImportParameters, imported_observation: Observation) -> None:
    imported_observation.product = import_parameters.product
    imported_observation.branch = import_parameters.branch
    imported_observation.parser = import_parameters.parser
    if not imported_observation.scanner:
        imported_observation.scanner = import_parameters.parser.name
    imported_observation.upload_filename = import_parameters.filename
    imported_observation.api_configuration_name = import_parameters.api_configuration_name
    imported_observation.import_last_seen = timezone.now()
    if import_parameters.service:
        imported_observation.origin_service_name = import_parameters.service
        service = Service.objects.get_or_create(product=import_parameters.product, name=import_parameters.service)[0]
        imported_observation.origin_service = service
    if import_parameters.docker_image_name_tag:
        imported_observation.origin_docker_image_name_tag = import_parameters.docker_image_name_tag
    if import_parameters.endpoint_url:
        imported_observation.origin_endpoint_url = import_parameters.endpoint_url
    if import_parameters.kubernetes_cluster:
        imported_observation.origin_kubernetes_cluster = import_parameters.kubernetes_cluster


def _process_current_observation(
    imported_observation: Observation, observation_before: Observation, settings: Settings
) -> None:
    # Set data in the current observation from the new observation
    observation_before.title = imported_observation.title
    observation_before.description = imported_observation.description
    observation_before.recommendation = imported_observation.recommendation
    observation_before.scanner_observation_id = imported_observation.scanner_observation_id
    observation_before.vulnerability_id = imported_observation.vulnerability_id
    observation_before.vulnerability_id_aliases = imported_observation.vulnerability_id_aliases
    observation_before.cvss3_score = imported_observation.cvss3_score
    observation_before.cvss3_vector = imported_observation.cvss3_vector
    observation_before.cvss4_score = imported_observation.cvss4_score
    observation_before.cvss4_vector = imported_observation.cvss4_vector
    observation_before.cwe = imported_observation.cwe
    observation_before.found = imported_observation.found
    observation_before.scanner = imported_observation.scanner

    observation_before.origin_component_dependencies = imported_observation.origin_component_dependencies

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
            observation_before.parser_status = _get_initial_status(observation_before.product)
    observation_before.current_status = get_current_status(observation_before)

    if observation_before.current_status == Status.STATUS_RISK_ACCEPTED:
        if previous_status != Status.STATUS_RISK_ACCEPTED:
            observation_before.risk_acceptance_expiry_date = calculate_risk_acceptance_expiry_date(
                observation_before.product
            )
    else:
        observation_before.risk_acceptance_expiry_date = None

    apply_epss(observation_before)
    apply_exploit_information(observation_before, settings)
    observation_before.import_last_seen = timezone.now()
    observation_before.save()

    observation_before.references.all().delete()
    if imported_observation.unsaved_references:
        for unsaved_reference in imported_observation.unsaved_references:
            reference = Reference(
                observation=observation_before,
                url=unsaved_reference,
            )
            clip_fields("core", "Reference", reference)
            reference.save()

    observation_before.evidences.all().delete()
    if imported_observation.unsaved_evidences:
        for unsaved_evidence in imported_observation.unsaved_evidences:
            evidence = Evidence(
                observation=observation_before,
                name=unsaved_evidence[0],
                evidence=unsaved_evidence[1],
            )
            clip_fields("core", "Evidence", evidence)
            evidence.save()

            # Write observation log if status or severity has been changed
    if previous_status != observation_before.current_status or previous_severity != observation_before.current_severity:
        status = observation_before.current_status if previous_status != observation_before.current_status else ""

        severity = (
            imported_observation.current_severity if previous_severity != observation_before.current_severity else ""
        )

        create_observation_log(
            observation=observation_before,
            severity=severity,
            status=status,
            comment="Updated by parser",
            vex_justification="",
            assessment_status=Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
            risk_acceptance_expiry_date=observation_before.risk_acceptance_expiry_date,
        )


def _process_new_observation(imported_observation: Observation, settings: Settings) -> None:
    imported_observation.current_severity = get_current_severity(imported_observation)

    if not imported_observation.parser_status:
        imported_observation.parser_status = _get_initial_status(imported_observation.product)

    imported_observation.current_status = get_current_status(imported_observation)

    imported_observation.risk_acceptance_expiry_date = (
        calculate_risk_acceptance_expiry_date(imported_observation.product)
        if imported_observation.current_status == Status.STATUS_RISK_ACCEPTED
        else None
    )

    # Observation has not been imported before, so it is a new one
    apply_epss(imported_observation)
    apply_exploit_information(imported_observation, settings)
    imported_observation.save()

    if imported_observation.unsaved_references:
        for unsaved_reference in imported_observation.unsaved_references:
            reference = Reference(
                observation=imported_observation,
                url=unsaved_reference,
            )
            clip_fields("core", "Reference", reference)
            reference.save()

    if imported_observation.unsaved_evidences:
        for unsaved_evidence in imported_observation.unsaved_evidences:
            evidence = Evidence(
                observation=imported_observation,
                name=unsaved_evidence[0],
                evidence=unsaved_evidence[1],
            )
            clip_fields("core", "Evidence", evidence)
            evidence.save()

    create_observation_log(
        observation=imported_observation,
        severity=imported_observation.current_severity,
        status=imported_observation.current_status,
        comment="Set by parser",
        vex_justification="",
        assessment_status=Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
        risk_acceptance_expiry_date=imported_observation.risk_acceptance_expiry_date,
    )


def _resolve_unimported_observations(
    observations_before: dict[str, Observation],
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
                observation=observation,
                severity="",
                status=observation.current_status,
                comment="Observation not found in latest scan",
                vex_justification="",
                assessment_status=Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
                risk_acceptance_expiry_date=None,
            )

    return observations_resolved


def _get_new_observations_in_review(product: Product) -> bool:
    if product.product_group and product.product_group.new_observations_in_review:
        return True
    return product.new_observations_in_review


def _get_initial_status(product: Product) -> str:
    if _get_new_observations_in_review(product):
        return Status.STATUS_IN_REVIEW
    return Status.STATUS_OPEN
