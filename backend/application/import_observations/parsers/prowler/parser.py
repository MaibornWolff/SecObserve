from json import load, dumps
from django.core.files.base import File

from application.core.models import Observation, Parser
from application.import_observations.parsers.base_parser import (
    BaseParser,
    BaseFileParser,
)


class ProwlerParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Prowler"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_DAST

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], None

        if not type(data) is list:
            return False, ["File is not a Prowler format, data is not a list"], None

        if len(data) >= 1:
            first_element = data[0]
            if type(first_element) is not dict:
                return (
                    False,
                    ["File is not a Prowler format, element is not a dictionary"],
                    None,
                )
            if not first_element.get("StatusExtended") or not first_element.get("Status"):
                return (
                    False,
                    [
                        "Data is not a Prowler format, element doesn't have a StatusExtended or Status entry"
                    ],
                    None,
                )

        return True, [], data

    def get_observations(self, data: list) -> list[Observation]:
        observations = []

        for prowler_observation in data:
            if prowler_observation.get("Status", "").lower() == "fail":
                check_title = prowler_observation.get("CheckTitle")
                status_extended = prowler_observation.get("StatusExtended")
                severity = prowler_observation.get("Severity", Observation.SEVERITY_UNKOWN).capitalize()
                if severity == "Informational":
                    severity = Observation.SEVERITY_NONE
                resource_type = prowler_observation.get("ResourceType")
                resource_id = prowler_observation.get("ResourceId")
                prowler_description = prowler_observation.get("Description")
                risk = prowler_observation.get("Risk")
                related_url = prowler_observation.get("RelatedUrl")
                recommendation_text = prowler_observation.get("Remediation", {}).get("Recommendation", {}).get("Text")
                recommendation_url = prowler_observation.get("Remediation", {}).get("Recommendation", {}).get("Url")
                recommendation_code = prowler_observation.get("Remediation", {}).get("Code")
                subscription = prowler_observation.get("Subscription")
                account_id = prowler_observation.get("AccountId")

                description = check_title
                if check_title != prowler_description:
                    description += f"\n\n{prowler_description}"
                if risk:
                    description += f"\n\n{risk}"
                if account_id:
                    description += f"\n\n**Account id:** {account_id}"
                if subscription:
                    description += f"\n\n**Subscription:** {subscription}"
                if resource_id:
                    description += f"\n\n**Resource id:** {resource_id}"
                if resource_type:
                    description += f"\n\n**Resource type:** {resource_type}"

                recommendation = None
                if recommendation_text:
                    recommendation = recommendation_text
                if recommendation_url:
                    recommendation += f"\n\n* {recommendation_url}"
                if recommendation_code:
                    for key in recommendation_code.keys():
                        if recommendation_code.get(key):
                            recommendation += f"\n\n* **{key}:** {recommendation_code.get(key)}"

                observation = Observation(
                    title=status_extended,
                    parser_severity=severity.title(), 
                    description=description,
                    recommendation=recommendation,
                )

                evidence = []
                evidence.append("Result")
                evidence.append(dumps(prowler_observation))
                observation.unsaved_evidences.append(evidence)

                if related_url:
                    observation.unsaved_references = [related_url]

                observations.append(observation)
        return observations
