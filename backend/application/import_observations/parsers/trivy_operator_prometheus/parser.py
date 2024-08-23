import json
from typing import Optional

import requests

from application.core.models import Observation
from application.core.types import Severity
from application.import_observations.models import Api_Configuration
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseParser,
)
from application.import_observations.types import Parser_Type


class TrivyOperatorPrometheus(BaseParser, BaseAPIParser):
    def __init__(self):
        self.api_configuration: Optional[Api_Configuration] = None

    @classmethod
    def get_name(cls) -> str:
        return "Trivy Operator Prometheus"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_OTHER

    def check_connection(
        self, api_configuration: Api_Configuration
    ) -> tuple[bool, list[str], dict]:
        self.api_configuration = api_configuration

        trivy_operator_prometheus_base_url = api_configuration.base_url
        trivy_operator_prometheus_query = api_configuration.query
        trivy_operator_prometheus_verify_ssl = api_configuration.verify_ssl
        trivy_operator_prometheus_basic_auth = api_configuration.basic_auth_enabled
        trivy_operator_prometheus_basic_auth_username = (
            api_configuration.basic_auth_username
        )
        trivy_operator_prometheus_basic_auth_password = (
            api_configuration.basic_auth_password
        )

        if not trivy_operator_prometheus_base_url.endswith("/"):
            trivy_operator_prometheus_base_url += "/"

        trivy_operator_prometheus_url = (
            trivy_operator_prometheus_base_url
            + "api/v1/query?query="
            + trivy_operator_prometheus_query
        )

        trivy_basic_auth_param = None
        if trivy_operator_prometheus_basic_auth:
            trivy_basic_auth_param = (
                trivy_operator_prometheus_basic_auth_username,
                trivy_operator_prometheus_basic_auth_password,
            )

        try:
            response = requests.get(
                trivy_operator_prometheus_url,
                timeout=60,
                verify=trivy_operator_prometheus_verify_ssl,
                auth=trivy_basic_auth_param,
            )
            response.raise_for_status()
        except Exception as e:
            return False, [f"Cannot access Prometheus: {str(e)}"], {}

        return True, [], response.json()

    def check_format(self, import_data) -> tuple[bool, list[str], dict]:
        try:
            data = json.load(import_data)
        except Exception:
            return False, ["Data is not valid JSON"], {}

        if not data.get("status") == "success":
            return False, ["Data is not a Prometheus API-Endpoint"], {}

        if not isinstance(data.get("data"), dict) or not isinstance(
            data.get("data").get("result"), list
        ):
            return False, ["Data not in valid Prometheus-Metric Format"], {}

        return True, [], data

    def __create_observation(self, finding) -> Observation:
        origin_component_name = finding.get("metric", {}).get("resource", "")
        vuln_title = finding.get("metric", {}).get("vuln_title", "")
        vulnerability_id = finding.get("metric", {}).get("vuln_id", "")
        cvss3_score = finding.get("metric", {}).get("vuln_score")
        severity = finding.get("metric", {}).get("severity", Severity.SEVERITY_UNKOWN)
        origin_docker_image_registry = finding.get("metric", {}).get(
            "image_registry", ""
        )
        origin_docker_image_repository = finding.get("metric", {}).get(
            "image_repository", ""
        )
        origin_docker_image_name = (
            origin_docker_image_registry + "/" + origin_docker_image_repository
        )
        origin_docker_image_tag = finding.get("metric", {}).get("image_tag", "")
        fixed_version = finding.get("metric", {}).get("fixed_version", "")
        origin_component_version = finding.get("metric", {}).get(
            "installed_version", ""
        )
        namespace = finding.get("metric", {}).get("namespace", "")
        resource_kind = finding.get("metric", {}).get("resource_kind", "")
        resource_name = finding.get("metric", {}).get("resource_name", "")
        prometheus_endpoint_url = (
            self.api_configuration.base_url
            if isinstance(self.api_configuration, Api_Configuration)
            else ""
        )

        observation = Observation(
            title=vulnerability_id,
            parser_severity=self.get_severity(severity),
            numerical_severity=cvss3_score,
            vulnerability_id=vulnerability_id,
            origin_docker_image_name=origin_docker_image_name,
            origin_docker_image_tag=origin_docker_image_tag,
            cvss3_score=cvss3_score,
            origin_component_name=origin_component_name,
            scanner="Trivy Operator",
            origin_component_version=origin_component_version,
            origin_kubernetes_namespace=namespace,
            origin_kubernetes_resource_type=resource_kind,
            origin_kubernetes_resource_name=resource_name,
            recommendation=self.get_recommendation(
                fixed_version, origin_component_version
            ),
            description=self.get_description(
                vuln_title=vuln_title,
                prometheus_endpoint_url=prometheus_endpoint_url,
            ),
        )

        return observation

    def get_observations(self, data) -> list[Observation]:
        observations = []

        for finding in data.get("data").get("result"):
            if not finding.get("metric", {}).get("vuln_id", ""):
                continue
            observation = self.__create_observation(finding)

            evidence = []
            evidence.append("Vulnerability")
            evidence.append(json.dumps(finding))
            observation.unsaved_evidences.append(evidence)

            observations.append(observation)

        return observations

    def get_description(
        self,
        vuln_title,
        prometheus_endpoint_url,
    ) -> str:
        description = vuln_title
        if prometheus_endpoint_url:
            description += f"\n\n**Prometheus host:** {prometheus_endpoint_url}"

        return description

    def get_recommendation(
        self,
        fixed_version,
        origin_component_version,
    ) -> str:
        recommendation = ""
        if fixed_version:
            recommendation += (
                f"Upgrade from **{origin_component_version}** to **{fixed_version}**"
            )

        return recommendation

    def get_severity(self, severity: str) -> str:
        if (
            severity.capitalize(),
            severity.capitalize(),
        ) in Severity.SEVERITY_CHOICES:
            return severity.capitalize()

        return Severity.SEVERITY_UNKOWN
