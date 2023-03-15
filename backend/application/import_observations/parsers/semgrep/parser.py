from json import load, dumps
from django.core.files.base import File

from application.core.models import Observation, Parser
from application.import_observations.parsers.base_parser import (
    BaseParser,
    BaseFileParser,
)

SEVERITIES = {
    "ERROR": Observation.SEVERITY_HIGH,
    "WARNING": Observation.SEVERITY_MEDIUM,
    "INFO": Observation.SEVERITY_NONE,
}


class SemgrepParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Semgrep"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_SAST

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], None

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        observations = []

        scanner = "Semgrep"
        version = data.get("version")
        if version:
            scanner += " / " + version

        for result in data.get("results", []):
            observation = self.create_observation(result, scanner)
            observations.append(observation)

        return observations

    def create_observation(self, result, scanner):
        check_id = result.get("check_id", "")
        lines = result.get("extra", {}).get("lines")
        message = result.get("extra", {}).get("message")
        confidence = result.get("extra", {}).get("metadata", {}).get("confidence")
        category = result.get("extra", {}).get("metadata", {}).get("category")
        cwe = self.get_cwe(result.get("extra", {}).get("metadata", {}).get("cwe"))
        impact = result.get("extra", {}).get("metadata", {}).get("impact")
        likelihood = result.get("extra", {}).get("metadata", {}).get("likelihood")
        references = result.get("extra", {}).get("metadata", {}).get("references", [])
        source = result.get("extra", {}).get("metadata", {}).get("source")
        severity = result.get("extra", {}).get("severity")
        path = result.get("path")
        end_line = result.get("end", {}).get("line")
        start_line = result.get("start", {}).get("line")

        description = ""
        if message:
            description += f"{message}\n\n"
        if lines:
            description += f"**Snippet:** ```{lines}```\n\n"
        if category:
            description += f"**Category:** {category}\n\n"
        if confidence:
            description += f"**Confidence:** {confidence}\n\n"
        if impact:
            description += f"**Impact:** {impact}\n\n"
        if likelihood:
            description += f"**Likelihood:** {likelihood}\n\n"

        observation = Observation(
            parser_severity=SEVERITIES.get(severity, Observation.SEVERITY_UNKOWN),
            title=check_id,
            description=description,
            origin_source_file=path,
            origin_source_line_start=self.get_int_or_none(start_line),
            origin_source_line_end=self.get_int_or_none(end_line),
            cwe=cwe,
            scanner=scanner,
        )

        evidence = []
        evidence.append("Result")
        evidence.append(dumps(result))
        observation.unsaved_evidences.append(evidence)

        observation.unsaved_references = []
        if source:
            observation.unsaved_references.append(source)
        for reference in references:
            observation.unsaved_references.append(reference)

        return observation

    def get_cwe(self, cwe):
        if cwe:
            if isinstance(cwe, list):
                cwe_string = cwe[0]
            elif isinstance(cwe, str):
                cwe_string = cwe
            else:
                return None

            if cwe_string.startswith("CWE-") and ":" in cwe_string:
                tag_parts = cwe_string.split(":")
                return self.get_int_or_none(tag_parts[0][4:])

        return None
