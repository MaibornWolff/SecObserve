import json
from typing import Optional

import requests

from application.core.models import Observation
from application.core.types import Severity, Status
from application.import_observations.models import Api_Configuration
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseParser,
)
from application.import_observations.types import Parser_Type

STATUS_MAPPING = {
    "NOT_SET": "",
    "EXPLOITABLE": Status.STATUS_OPEN,
    "IN_TRIAGE": Status.STATUS_IN_REVIEW,
    "RESOLVED": Status.STATUS_RESOLVED,
    "FALSE_POSITIVE": Status.STATUS_FALSE_POSITIVE,
    "NOT_AFFECTED": Status.STATUS_NOT_AFFECTED,
}


class TrivyPrometheus(BaseParser, BaseAPIParser):
    def __init__(self):
        self.api_configuration: Optional[Api_Configuration] = None

    @classmethod
    def get_name(cls) -> str:
        return "Trivy Prometheus"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_OTHER

    def check_connection(
        self, api_configuration: Api_Configuration
    ) -> tuple[bool, list[str], dict]:
        self.api_configuration = api_configuration

        trivy_prometheus_base_url = api_configuration.base_url
        trivy_prometheus_query = api_configuration.query

        if not trivy_prometheus_base_url.endswith("/"):
            trivy_prometheus_base_url += "/"

        trivy_prometheus_url = trivy_prometheus_base_url + "api/v1/query?query=" + trivy_prometheus_query

        try:
            print(trivy_prometheus_base_url)
            response = requests.get(
                trivy_prometheus_url, timeout=60, verify=False
            )
            response.raise_for_status()
        except Exception as e:
            return False, [f"Cannot access Prometheus: {str(e)}"], {}

        return True, [], response.json().get("data").get("result")

    def get_observations(self, data: list[dict]) -> list[Observation]:
        observations = []

        scanner, version = self.get_about()
        if version:
            scanner += " / " + version

        for finding in data:
            origin_component_name = finding.get("metric", {}).get("resource", "")
            vuln_title = finding.get("metric", {}).get("vuln_title", "")
            vulnerability_id = finding.get("metric", {}).get("vuln_id", "")
            cvss3_score = finding.get("metric", {}).get("vuln_score")
            severity = finding.get("metric", {}).get("severity", Severity.SEVERITY_UNKOWN)
            origin_docker_image_name = finding.get("metric", {}).get("image_registry", "") + "/" + finding.get("metric", {}).get("image_repository", "")
            origin_docker_image_tag = finding.get("metric", {}).get("image_tag", "")
            fixed_version = finding.get("metric", {}).get("fixed_version", "")
            installed_version = finding.get("metric", {}).get("installed_version", "")

            state = ""
            reference_url = ""
            cwes = ""

            observation = Observation(
                title=vulnerability_id,
                parser_severity=self.get_severity(severity),
                numerical_severity=cvss3_score,
                parser_status=self.get_status(state),
                vulnerability_id=vulnerability_id,
                origin_docker_image_name=origin_docker_image_name,
                origin_docker_image_tag=origin_docker_image_tag,
                cvss3_score=cvss3_score,
                origin_component_name=origin_component_name,
                cwe=self.get_cwe(cwes),
                scanner=scanner,
                recommendation=self.get_recommendation(fixed_version,installed_version),
                description=self.get_description(vuln_title),
            )

            evidence = []
            evidence.append("Vulnerability")
            evidence.append(json.dumps(finding))
            observation.unsaved_evidences.append(evidence)

            if reference_url:
                observation.unsaved_references = [reference_url]

            observations.append(observation)

        return observations
    
    def get_description(  # pylint: disable=too-many-branches
        self,
        vuln_title,
    ) -> str:
        description = ""
        description +=  f"**Title:** {vuln_title}\n\n"
        return description

    def get_recommendation(  # pylint: disable=too-many-branches
        self,
        fixed_version,
        installed_version,
    ) -> str:
        recommendation = ""
        if fixed_version:
            recommendation +=  f"Upgrade from **{installed_version}** to: **{fixed_version}**\n\n"

        return recommendation

    def get_status(self, state: str) -> str:
        if not state:
            return ""

        return STATUS_MAPPING.get(state, "")

    def get_severity(self, severity: str) -> str:
        if (
            severity.capitalize(),
            severity.capitalize(),
        ) in Severity.SEVERITY_CHOICES:
            return severity.capitalize()

        return Severity.SEVERITY_UNKOWN

    def get_cwe(self, cwes: list[dict]) -> int | None:
        if cwes:
            return cwes[0].get("cweId")

        return None

    def get_about(self) -> tuple[str, Optional[str]]:
        if not self.api_configuration:
            return "Trivy-Prometheus", None

        trivy_prometheus_base_url = self.api_configuration.base_url
        if not trivy_prometheus_base_url.endswith("/"):
            trivy_prometheus_base_url += "/"

        try:
            response = requests.get(trivy_prometheus_base_url, timeout=60)
            response.raise_for_status()
        except Exception:
            return "Trivy-Prometheus", None

        application = "Trivy-Prometheus"
        version = 1

        return application, version
