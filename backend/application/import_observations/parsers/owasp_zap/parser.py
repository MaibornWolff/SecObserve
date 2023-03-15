from json import load, dumps
from django.core.files.base import File

from application.core.models import Observation, Parser
from application.import_observations.parsers.base_parser import (
    BaseParser,
    BaseFileParser,
)

SEVERITIES = {
    "0": Observation.SEVERITY_NONE,
    "1": Observation.SEVERITY_LOW,
    "2": Observation.SEVERITY_MEDIUM,
    "3": Observation.SEVERITY_HIGH,
    "4": Observation.SEVERITY_CRITICAL,
}


class SecObserveParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "OWASP ZAP"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_DAST

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], None

        if not data.get("@programName") == "OWASP ZAP":
            return False, ["File is not an OWASP ZAP format"], None

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        observations = []

        data_program_name = data.get("@programName")
        data_version = data.get("@version")
        if data_version:
            data_scanner = f"{data_program_name} / {data_version}"
        else:
            data_scanner = f"{data_program_name}"

        for site in data.get("site", []):
            data_origin_endpoint_url = site.get("@name")
            for alert in site.get("alerts"):
                data_title = alert.get("alert")
                data_severity = SEVERITIES.get(
                    alert.get("riskcode"), Observation.SEVERITY_UNKOWN
                )
                data_description = alert.get("desc", "")

                data_otherinfo = alert.get("otherinfo")
                if data_otherinfo:
                    data_description += f"\n\n**Other info:** {data_otherinfo}"

                data_amount_instances = alert.get("count")
                if data_amount_instances:
                    data_description += (
                        f"\n\n**Amount of instances:** {data_amount_instances}"
                    )

                data_first_instance = alert.get("instances", [])[0]
                if data_first_instance:
                    data_instance_uri = data_first_instance.get("uri")
                    if data_instance_uri:
                        data_description += "\n\n**First instance:**"
                        data_description += f"\n* **URI:** {data_instance_uri}"
                    data_instance_method = data_first_instance.get("method")
                    if data_instance_method:
                        data_description += f"\n* **Method:** {data_instance_method}"
                    data_instance_param = data_first_instance.get("param")
                    if data_instance_param:
                        data_description += f"\n* **Param:** {data_instance_param}"
                    data_instance_attack = data_first_instance.get("attack")
                    if data_instance_attack:
                        data_description += f"\n* **Attack:** {data_instance_attack}"
                    data_instance_evidence = data_first_instance.get("evidence")
                    if data_instance_evidence:
                        data_description += (
                            f"\n* **Evidence:** {data_instance_evidence}"
                        )

                data_recommendation = alert.get("solution")
                data_cwe = alert.get("cweid")
                if data_cwe == "-1":
                    data_cwe = None

                observation = Observation(
                    title=data_title,
                    description=data_description,
                    recommendation=data_recommendation,
                    parser_severity=data_severity,
                    origin_endpoint_url=data_origin_endpoint_url,
                    cwe=data_cwe,
                    scanner=data_scanner,
                )

                data_references = alert.get("reference")
                if data_references:
                    data_references = data_references.replace("</p><p>", "|")
                    data_references = data_references.replace("<p>", "")
                    data_references = data_references.replace("</p>", "")
                    for data_reference in data_references.split("|"):
                        observation.unsaved_references.append(
                            data_reference.split(" ")[0]
                        )

                evidence = []
                evidence.append("Alert")
                evidence.append(dumps(alert))
                observation.unsaved_evidences.append(evidence)

                observations.append(observation)

        return observations
