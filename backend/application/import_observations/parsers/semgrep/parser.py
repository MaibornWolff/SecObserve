from json import dumps, load

from django.core.files.base import File

from application.core.models import Observation
from application.core.types import Severity
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Type

SEVERITIES = {
    "error": Severity.SEVERITY_HIGH,
    "warning": Severity.SEVERITY_MEDIUM,
    "info": Severity.SEVERITY_LOW,
}


class SemgrepParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Semgrep"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_SAST

    def check_format(self, file: File) -> tuple[bool, list[str], dict | list]:
        try:  # pylint: disable=duplicate-code
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], {}

        if not data.get("version"):
            return False, ["File is not a Semgrep format, version is missing"], {}

        if not isinstance(data.get("results"), list):
            return False, ["File is not a Semgrep format, data is not a list"], {}

        if len(data.get("results")) >= 1:  # pylint: disable=duplicate-code
            first_element = data.get("results")[0]
            if not isinstance(first_element, dict):
                return (
                    False,
                    ["File is not a Semgrep format, element is not a dictionary"],
                    {},
                )
            if not first_element.get("check_id"):
                return (
                    False,
                    [
                        "Data is not a Semgrep format, element doesn't have a check_id entry"
                    ],
                    {},
                )

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        observations = []

        version = data.get("version")

        for result in data.get("results", {}):
            extra = result.get("extra", {})
            metadata = extra.get("metadata", {})
            category = metadata.get("category")
            if category.lower() != "security":
                continue

            check_id = result.get("check_id")
            path = result.get("path")
            start_line = None
            end_line = None
            if path:
                start_line = result.get("start", {}).get("line")
                end_line = result.get("end", {}).get("line")
            severity = extra.get("severity")
            engine_kind = extra.get("engine_kind")
            fix = extra.get("fix")
            if fix:
                fix = f"```\n{fix}\n```"

            so_severity = SEVERITIES.get(severity.lower(), Severity.SEVERITY_UNKNOWN)

            scanner = self.get_name()
            if engine_kind:
                scanner = f"{scanner} ({engine_kind})"
            scanner = f"{scanner} / {version}"

            observation = Observation(
                title=check_id,
                description=self._get_description(result),
                recommendation=fix,
                parser_severity=so_severity,
                origin_source_file=path,
                origin_source_line_start=start_line,
                origin_source_line_end=end_line,
                scanner=scanner,
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(result))
            observation.unsaved_evidences.append(evidence)

            observation.unsaved_references = self._get_references(result)

            observations.append(observation)

        return observations

    def _get_description(self, result: dict) -> str:
        extra = result.get("extra", {})
        message = extra.get("message")
        metadata = extra.get("metadata", {})
        vulnerability_class = metadata.get("vulnerability_class", [])

        description = f"{message}"

        if len(vulnerability_class) == 1:
            description += f"\n\n**Vulnerability Class:** {vulnerability_class[0]}"
        if len(vulnerability_class) > 1:
            description += (
                f"\n\n**Vulnerability Classes:** {', '.join(vulnerability_class)}"
            )

        return description

    def _get_references(self, result: dict) -> list[str]:
        so_references = []

        extra = result.get("extra", {})
        metadata = extra.get("metadata", {})
        references = metadata.get("references")
        source = metadata.get("source")
        references = metadata.get("references", [])

        if source:
            so_references.append(source)
        so_references.extend(references)

        return so_references
