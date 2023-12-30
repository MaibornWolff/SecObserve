import csv
import io
from json import dumps

from django.core.files.base import File

from application.core.models import Observation, Parser
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)


class AzureDefenderParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Azure Defender"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_INFRASTRUCTURE

    def check_format(self, file: File) -> tuple[bool, list[str], dict | list]:
        if file.name and not file.name.endswith(".csv"):
            return False, ["File is not CSV"], {}
        try:
            content = file.read()
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            reader = csv.DictReader(io.StringIO(content), delimiter=",", quotechar='"')
        except Exception:
            return False, ["File is not valid CSV"], {}

        rows = []
        for row in reader:
            rows.append(row)

        if rows:
            if not rows[0].get("subscriptionName"):
                return False, ["File is not an Azure Defender export"], {}

        return True, [], rows

    def get_observations(self, data: list[dict]) -> list[Observation]:
        observations = []

        for row in data:
            state = row.get("state", "").lower()
            if state == "unhealthy":
                subscriptionName = row.get("subscriptionName", "")
                resourceType = row.get("resourceType", "")
                resourceName = row.get("resourceName", "")
                recommendationDisplayName = row.get("recommendationDisplayName", "")
                description = row.get("description", "")
                remediationSteps = row.get("remediationSteps", "")
                severity = row.get("severity", "")
                cloud = row.get("cloud", "")

                observation = Observation(
                    title=recommendationDisplayName,
                    description=description,
                    recommendation=remediationSteps,
                    parser_severity=severity,
                    origin_cloud_provider=cloud,
                    origin_cloud_account_subscription_project=subscriptionName,
                    origin_cloud_resource=resourceName,
                    origin_cloud_resource_type=resourceType,
                    scanner=self.get_name(),
                )

                evidence = []
                evidence.append("Result")
                evidence.append(dumps(row))
                observation.unsaved_evidences.append(evidence)

                observations.append(observation)

        return observations
