import logging
from json import load

from django.core.files.base import File
from py_ocsf_models.events.findings.detection_finding import (
    ClassUID,
    DetectionFinding,
    StatusID,
)
from py_ocsf_models.events.findings.finding import ActivityID

from application.core.models import Observation
from application.core.types import Severity
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.parsers.ocsf.types import Origin
from application.import_observations.types import Parser_Type

logger = logging.getLogger("secobserve.import_observations.parsers.ocsf")


class OCSFParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "OCSF (Open Cybersecurity Schema Framework)"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_INFRASTRUCTURE

    def check_format(self, file: File) -> tuple[bool, list[str], dict | list]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], {}

        if not isinstance(data, list):
            return False, ["File is not a OCSF format, data is not a list"], {}

        if len(data) >= 1:
            first_element = data[0]
            if not isinstance(first_element, dict):
                return (
                    False,
                    ["File is not a OCSF format, element is not a dictionary"],
                    {},
                )
            if not first_element.get("finding_info"):
                return (
                    False,
                    [
                        "File is not a OCSF format, first element doesn't have a finding_info entry"
                    ],
                    {},
                )

        return True, [], data

    def get_observations(self, data: list) -> list[Observation]:
        observations = []

        for element in data:
            if element.get("class_uid") != ClassUID.DetectionFinding:
                logger.info(
                    "Class UID %s is not supported, only %s / DetectionFinding",
                    element.get("class_uid"),
                    ClassUID.DetectionFinding,
                )
                continue

            try:
                finding = DetectionFinding.parse_obj(element)

                if finding.status_id not in [StatusID.New, StatusID.InProgress]:
                    continue

                if finding.activity_id not in [ActivityID.Create, ActivityID.Update]:
                    continue

                if not finding.finding_info:
                    logging.info("OCSF finding has no finding_info")
                    continue

                for origin in get_origins(finding):
                    observation = Observation(
                        title=finding.finding_info.title,
                        description=get_description(finding),
                        origin_cloud_provider=origin.origin_cloud_provider,
                        origin_cloud_account_subscription_project=origin.origin_cloud_account_subscription_project,
                        origin_cloud_resource=origin.origin_cloud_resource,
                        origin_cloud_resource_type=origin.origin_cloud_resource_type,
                        origin_kubernetes_namespace=origin.origin_kubernetes_namespace,
                        origin_kubernetes_resource_type=origin.origin_kubernetes_resource_type,
                        origin_kubernetes_resource_name=origin.origin_kubernetes_resource_name,
                        parser_severity=get_severity(finding),
                        recommendation=get_recommentation(finding),
                        scanner=get_scanner(finding),
                    )

                    observations.append(observation)

                    evidence = []
                    evidence.append("OCSF Finding")
                    evidence.append(finding.json(exclude_none=True))
                    observation.unsaved_evidences.append(evidence)

                    observation.unsaved_references = get_references(finding)
            except Exception as e:
                logger.warning("Error parsing OCSF finding: %s", str(e))

        return observations


def get_origins(finding: DetectionFinding) -> list[Origin]:
    origins: list[Origin] = []

    if not finding.resources:
        return origins

    if finding.finding_info.uid.startswith("prowler-kubernetes"):
        for resource in finding.resources:
            namespace = ""
            if resource.region and ":" in resource.region:
                namespace = resource.region.split(":")[1].strip()
            origins.append(
                Origin(
                    origin_kubernetes_namespace=namespace,
                    origin_kubernetes_resource_type=resource.type,
                    origin_kubernetes_resource_name=resource.name,
                )
            )
    elif finding.cloud:
        account_name = ""
        if finding.cloud.account:
            account_name = finding.cloud.account.name
        for resource in finding.resources:
            origins.append(
                Origin(
                    origin_cloud_provider=finding.cloud.provider.capitalize(),
                    origin_cloud_account_subscription_project=account_name,
                    origin_cloud_resource=resource.name,
                    origin_cloud_resource_type=resource.type,
                )
            )

    return origins


def get_description(finding: DetectionFinding) -> str:
    description = finding.finding_info.desc

    if finding.status_detail:
        description += f"\n\n**Status detail:** {finding.status_detail}"
    if finding.risk_details:
        description += f"\n\n**Risk details:** {finding.risk_details}"
    if finding.unmapped and finding.unmapped.get("notes"):
        description += f"\n\n**Notes:** {finding.unmapped['notes']}"

    return description


def get_recommentation(finding: DetectionFinding) -> str:
    if finding.remediation:
        return finding.remediation.desc

    return ""


def get_references(finding: DetectionFinding) -> list[str]:
    references = []

    if finding.unmapped and finding.unmapped.get("related_url"):
        references.append(finding.unmapped["related_url"])

    if finding.remediation and finding.remediation.references:
        for reference in finding.remediation.references:
            if reference.startswith("http") and reference not in references:
                references.append(reference)

    return references


def get_scanner(finding: DetectionFinding) -> str:
    scanner = ""

    if finding.metadata and finding.metadata.product and finding.metadata.product:
        scanner = finding.metadata.product.name
        if finding.metadata.product.version:
            scanner += f" / {finding.metadata.product.version}"

    return scanner


def get_severity(finding: DetectionFinding) -> str:
    if finding.severity:
        severity = finding.severity.capitalize()
        if (severity, severity) in Severity.SEVERITY_CHOICES:
            return finding.severity.capitalize()

    return Severity.SEVERITY_UNKOWN
