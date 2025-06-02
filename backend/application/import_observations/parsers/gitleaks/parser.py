from json import dumps
from typing import Any, Optional

from application.core.models import Branch, Observation, Product
from application.core.types import Severity
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Filetype, Parser_Type


class GitleaksParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "Gitleaks"

    @classmethod
    def get_filetype(cls) -> str:
        return Parser_Filetype.FILETYPE_JSON

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_SECRETS

    def check_format(self, data: Any) -> bool:
        if (
            isinstance(data, list)  # pylint: disable=too-many-boolean-expressions
            and len(data) >= 1
            and isinstance(data[0], dict)
            and data[0].get("RuleID")
            and data[0].get("Match")
            and data[0].get("Secret")
        ):
            return True
        return False

    def get_observations(self, data: list, product: Product, branch: Optional[Branch]) -> tuple[list[Observation], str]:
        observations = []

        for entry in data:
            rule_id = entry.get("RuleID")
            description = entry.get("Description")
            start_line = entry.get("StartLine")
            end_line = entry.get("EndLine")
            match = entry.get("Match")
            secret = entry.get("Secret")
            file = entry.get("File")
            link = entry.get("Link")
            commit = entry.get("Commit")
            date = entry.get("Date")
            message = entry.get("Message")

            if match:
                if secret:
                    match = match.replace(secret, "REDACTED")
                description += f"\n\n**Match:** `{match}`"

            if commit:
                description += f"\n\n**Commit hash:** {commit}"
                if date:
                    description += f"\n\n**Commit date:** {date}"
                if message:
                    if message.find("\n") >= 0:
                        message = message.split("\n")[0] + " ..."
                    description += f"\n\n**Commit message:** {message}"

            observation = Observation(
                title=rule_id,
                parser_severity=Severity.SEVERITY_MEDIUM,
                description=description,
                origin_source_file=file,
                origin_source_line_start=self.get_int_or_none(start_line),
                origin_source_line_end=self.get_int_or_none(end_line),
                origin_source_file_link=link,
            )

            evidence = []
            evidence.append("Entry")
            evidence_string = dumps(entry)
            if secret:
                evidence_string = evidence_string.replace(secret, "REDACTED")
            evidence.append(evidence_string)

            observation.unsaved_evidences.append(evidence)

            observations.append(observation)

        return observations, self.get_name()
