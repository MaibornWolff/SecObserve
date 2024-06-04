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
            component = finding.get("metric", {}).get("resource", "")
            image = finding.get("metric", {}).get("image_repository", "")
            component_name = component + ": " + image
            component_version = finding.get("metric", {}).get("image_tag", "")
            vuln_title = finding.get("metric", {}).get("vuln_title", "")
            vulnerability_id = finding.get("metric", {}).get("vuln_id", "")
            cvss_v3_base_score = finding.get("metric", {}).get("vuln_score")
            severity = finding.get("metric", {}).get("severity", Severity.SEVERITY_UNKOWN)
            description = self.get_description(
                component_version, vulnerability_id, cvss_v3_base_score, vuln_title, image, component
            )

            state = ""
            reference_url = ""
            cwes = ""

            observation = Observation(
                title=vulnerability_id,
                description=description,
                parser_severity=self.get_severity(severity),
                parser_status=self.get_status(state),
                vulnerability_id=vulnerability_id,
                origin_component_name=component_name,
                origin_component_version=component_version,
                cvss3_score=cvss_v3_base_score,
                cwe=self.get_cwe(cwes),
                scanner=scanner,
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
        component_version: str,
        vulnerability_id: str,
        cvss_v3_base_score: str,
        vuln_title: str,
        image: str,
        component: str,
    ) -> str:
        description = ""

        description += f"**Component**: {component}\n\n"
        description += f"**Rule full description**: {vuln_title}\n\n"
        description += f"**Security-Severity**: {cvss_v3_base_score}\n\n"
        description += f"**CVE**: [{vulnerability_id}](https://nvd.nist.gov/vuln/detail/{vulnerability_id})\n\n"
        description += f"**Image**: {image}:{component_version}\n\n"

        return description

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
