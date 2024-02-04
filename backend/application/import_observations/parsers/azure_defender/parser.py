import csv
import io
import re
from json import dumps

from django.core.files.base import File

from application.core.models import Observation
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Type


class AzureDefenderParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Azure Defender"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_INFRASTRUCTURE

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
                description = self.format_markdown(description)
                remediationSteps = row.get("remediationSteps", "")
                remediationSteps = self.format_markdown(remediationSteps)
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

    def format_markdown(self, string: str) -> str:
        string = self.replace_string_with_newlines(string, r"\.[A-Z]")
        string = self.replace_string_with_newlines(string, r"\:[A-Z]")
        string = self.replace_string_with_newlines(string, r"\.[1-9]\.")
        string = self.replace_string_with_newlines(string, r"\:[1-9]\.")
        string = self.replace_string_with_newlines(string, r" [1-9]\.")
        return string

    def replace_string_with_newlines(self, string: str, regex: str) -> str:
        match: re.Match[str] | None | str = "initial_match"
        while match:
            match = re.search(regex, string)
            if match:
                string = (
                    string[: match.start() + 1]
                    + "\n\n"
                    + string[match.start() + 1 :]  # noqa: E203
                    # black inserts a space before the colon
                )
        return string
