import re
from json import dumps
from typing import Optional

from application.core.models import Branch, Observation, Product
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Filetype, Parser_Type


class AzureDefenderParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Azure Defender"

    @classmethod
    def get_filetype(cls) -> str:
        return Parser_Filetype.FILETYPE_CSV

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_INFRASTRUCTURE

    def check_format(self, data: list[dict]) -> bool:
        if data and data[0].get("subscriptionId") and data[0].get("subscriptionName"):
            return True
        return False

    def get_observations(
        self, data: list[dict], product: Product, branch: Optional[Branch]
    ) -> tuple[list[Observation], str]:
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

        return observations, self.get_name()

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
