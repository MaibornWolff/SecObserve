import json
from typing import Optional

import requests

from application.core.models import Observation, Parser
from application.import_observations.models import Api_Configuration
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseParser,
)

STATUS_MAPPING = {
    "NOT_SET": "",
    "EXPLOITABLE": Observation.STATUS_OPEN,
    "IN_TRIAGE": Observation.STATUS_IN_REVIEW,
    "RESOLVED": Observation.STATUS_RESOLVED,
    "FALSE_POSITIVE": Observation.STATUS_FALSE_POSITIVE,
    "NOT_AFFECTED": Observation.STATUS_NOT_AFFECTED,
}


class DependencyTrack(BaseParser, BaseAPIParser):
    @classmethod
    def get_name(cls) -> str:
        return "Dependency Track"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_SCA

    def check_connection(
        self, api_configuration: Api_Configuration
    ) -> tuple[bool, list[str], dict]:
        self.api_configuration = api_configuration

        dependency_track_base_url = api_configuration.base_url
        dependency_track_api_key = api_configuration.api_key
        dependency_track_project_key = api_configuration.project_key

        if not dependency_track_base_url.endswith("/"):
            dependency_track_base_url += "/"

        dependency_track_base_url += (
            f"api/v1/finding/project/{dependency_track_project_key}?suppressed=false"
        )

        headers = {
            "X-Api-Key": dependency_track_api_key,
        }
        try:
            response = requests.get(
                dependency_track_base_url, headers=headers, timeout=60
            )
            response.raise_for_status()
        except Exception as e:
            return False, [f"Cannot access Dependency Track API: {str(e)}"], {}

        return True, [], response.json()

    def get_observations(self, data: list[dict]) -> list[Observation]:
        observations = []

        scanner, version = self.get_about()
        if version:
            scanner += " / " + version

        for finding in data:
            component_name = finding.get("component", []).get("name")
            component_version = finding.get("component", []).get("version")
            component_purl = finding.get("component", []).get("purl")
            component_cpe = finding.get("component", []).get("cpe")

            vulnerability_id = finding.get("vulnerability", {}).get("vulnId", "")
            cvss_v3_base_score = finding.get("vulnerability", {}).get("cvssV3BaseScore")
            cvss_v3_vector = finding.get("vulnerability", {}).get("cvssV3Vector")
            severity = finding.get("vulnerability", {}).get(
                "severity", Observation.SEVERITY_UNKOWN
            )
            description = finding.get("vulnerability", {}).get("description")

            state = finding.get("analysis", {}).get("state")
            reference_url = finding.get("attribution", {}).get("referenceUrl")
            cwes = finding.get("cwes", [])

            observation = Observation(
                title=vulnerability_id,
                description=description,
                parser_severity=self.get_severity(severity),
                parser_status=self.get_status(state),
                vulnerability_id=vulnerability_id,
                origin_component_name=component_name,
                origin_component_version=component_version,
                origin_component_purl=component_purl,
                origin_component_cpe=component_cpe,
                cvss3_score=cvss_v3_base_score,
                cvss3_vector=cvss_v3_vector,
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

    def get_status(self, state: str) -> str:
        if not state:
            return ""

        return STATUS_MAPPING.get(state, "")

    def get_severity(self, severity: str) -> str:
        if (
            severity.capitalize(),
            severity.capitalize(),
        ) in Observation.SEVERITY_CHOICES:
            return severity.capitalize()

        return Observation.SEVERITY_UNKOWN

    def get_cwe(self, cwes: list[dict]) -> int | None:
        if cwes:
            return cwes[0].get("cweId")

        return None

    def get_about(self) -> tuple[str, Optional[str]]:
        dependency_track_base_url = self.api_configuration.base_url
        if not dependency_track_base_url.endswith("/"):
            dependency_track_base_url += "/"
        dependency_track_base_url += "api/version"

        try:
            response = requests.get(dependency_track_base_url, timeout=60)
            response.raise_for_status()
        except Exception:
            return "Dependency-Track", None

        application = response.json().get("application", "Dependency-Track")
        version = response.json().get("version")

        return application, version
