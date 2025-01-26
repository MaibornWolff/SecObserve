from json import dumps
from typing import Any, Optional

from application.core.models import Branch, Observation, Product
from application.core.types import Severity
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Filetype, Parser_Type


class ProwlerParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Prowler 3"

    @classmethod
    def get_filetype(cls) -> str:
        return Parser_Filetype.FILETYPE_JSON

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_INFRASTRUCTURE

    def check_format(self, data: Any) -> bool:
        if (
            isinstance(data, list)
            and len(data) >= 1
            and isinstance(data[0], dict)
            and data[0].get("StatusExtended")
            and data[0].get("Status")
        ):
            return True
        return False

    def get_observations(  # pylint: disable=too-many-locals
        self, data: list[dict], product: Product, branch: Optional[Branch]
    ) -> list[Observation]:
        observations = []

        for prowler_observation in data:
            if prowler_observation.get("Status", "").lower() == "fail":
                status_extended = prowler_observation.get(
                    "StatusExtended", "No StatusExtended found"
                )
                severity = prowler_observation.get(
                    "Severity", Severity.SEVERITY_UNKNOWN
                ).capitalize()
                if severity == "Informational":
                    severity = Severity.SEVERITY_NONE

                description = self.get_description(prowler_observation)
                recommendation = self.get_recommendation(prowler_observation)

                provider = prowler_observation.get("Provider", "")
                if provider == "aws":
                    provider = "AWS"
                else:
                    provider = provider.title()

                account_id = prowler_observation.get("AccountId")
                account_name = prowler_observation.get("AccountName")
                subscription = prowler_observation.get("Subscription")
                account_subscription_project = ""
                if account_name:
                    account_subscription_project = account_name
                elif account_id:
                    account_subscription_project = account_id
                elif subscription:
                    account_subscription_project = subscription

                resource_id = prowler_observation.get("ResourceId")
                resource_name = prowler_observation.get("ResourceName")
                resource = ""
                if resource_name:
                    resource = resource_name
                elif resource_id:
                    resource = resource_id

                resource_type = prowler_observation.get("ResourceType", "")

                observation = Observation(
                    title=status_extended,
                    parser_severity=severity.title(),
                    description=description,
                    recommendation=recommendation,
                    origin_cloud_provider=provider,
                    origin_cloud_account_subscription_project=account_subscription_project,
                    origin_cloud_resource=resource,
                    origin_cloud_resource_type=resource_type,
                )

                evidence = []
                evidence.append("Result")
                evidence.append(dumps(prowler_observation))
                observation.unsaved_evidences.append(evidence)

                related_url = prowler_observation.get("RelatedUrl")
                if related_url:
                    observation.unsaved_references = [related_url]

                observations.append(observation)

        return observations

    def get_description(self, prowler_observation: dict) -> str:
        check_title = prowler_observation.get("CheckTitle")
        prowler_description = prowler_observation.get("Description")
        risk = prowler_observation.get("Risk")

        description = check_title if check_title else ""
        if check_title != prowler_description:
            description += f"\n\n{prowler_description}"
        if risk:
            description += f"\n\n{risk}"
        return description

    def get_recommendation(self, prowler_observation: dict) -> str:
        recommendation_text = (
            prowler_observation.get("Remediation", {})
            .get("Recommendation", {})
            .get("Text")
        )
        recommendation_url = (
            prowler_observation.get("Remediation", {})
            .get("Recommendation", {})
            .get("Url")
        )
        recommendation_code = prowler_observation.get("Remediation", {}).get("Code")
        recommendation = ""
        if recommendation_text:
            recommendation = recommendation_text
        if recommendation_url:
            recommendation += f"\n\n* {recommendation_url}"
        if recommendation_code:
            for key in recommendation_code.keys():
                if recommendation_code.get(key):
                    recommendation += f"\n\n* **{key}:** {recommendation_code.get(key)}"

        return recommendation
