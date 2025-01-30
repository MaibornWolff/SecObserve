from dataclasses import dataclass
from json import dumps
from typing import Any, Optional, Tuple

from packageurl import PackageURL

from application.core.models import Branch, Observation, Product
from application.core.types import Severity
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Filetype, Parser_Type

SEVERITIES = {
    "error": Severity.SEVERITY_HIGH,
    "warning": Severity.SEVERITY_MEDIUM,
    "note": Severity.SEVERITY_LOW,
    "none": Severity.SEVERITY_NONE,
}


@dataclass
class Rule:
    default_level: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    help_uri: Optional[str] = None
    help: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    properties: Optional[str] = None
    rule_dict: Optional[str] = None


@dataclass
class Location:
    uri: str = ""
    start_line: Optional[str] = None
    end_line: Optional[str] = None
    snippet: Optional[str] = None


class SARIFParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "SARIF"

    @classmethod
    def get_filetype(cls) -> str:
        return Parser_Filetype.FILETYPE_JSON

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_SAST

    def check_format(self, data: Any) -> bool:
        if (
            isinstance(data, dict)
            and "sarif" in data.get("$schema", "").lower()
            and data.get("version") == "2.1.0"
        ):
            return True
        return False

    def get_observations(
        self, data: dict, product: Product, branch: Optional[Branch]
    ) -> list[Observation]:
        observations: list[Observation] = []

        for run in data.get("runs", []):
            sarif_scanner = run.get("tool", {}).get("driver", {}).get("name")
            sarif_version = run.get("tool", {}).get("driver", {}).get("version")
            if not sarif_version:
                sarif_version = (
                    run.get("tool", {}).get("driver", {}).get("semanticVersion")
                )
            if sarif_version:
                sarif_scanner += " / " + sarif_version

            sarif_rules = self.get_rules(run)
            for result in run.get("results", []):
                if result.get("kind", "fail") != "fail":
                    # see §3.27.9 kind property
                    continue

                if self.result_is_suppressed(result):
                    # see §3.27.23 suppressions property
                    continue

                sarif_locations = result.get("locations", [])
                if sarif_locations:
                    for sarif_location in result.get("locations", []):
                        self.create_observation(
                            result=result,
                            observations=observations,
                            sarif_scanner=sarif_scanner,
                            sarif_rules=sarif_rules,
                            sarif_location=sarif_location,
                        )
                else:
                    self.create_observation(
                        result=result,
                        observations=observations,
                        sarif_scanner=sarif_scanner,
                        sarif_rules=sarif_rules,
                        sarif_location=None,
                    )

        return observations

    def create_observation(  # pylint: disable=too-many-locals
        self,
        *,
        result: dict,
        observations: list[Observation],
        sarif_scanner: str,
        sarif_rules: dict[str, Rule],
        sarif_location: Optional[dict],
    ):
        location = self.get_location_data(sarif_location)

        sarif_rule_id = result.get("ruleId", "")
        sarif_rule = sarif_rules.get(sarif_rule_id, Rule())

        parser_severity = self.get_parser_severity(result, sarif_scanner, sarif_rule)

        parser_cvss3_score, parser_cvss3_vector = self.get_dependency_check_cvss(
            sarif_scanner, sarif_rule, 3
        )
        parser_cvss4_score, parser_cvss4_vector = self.get_dependency_check_cvss(
            sarif_scanner, sarif_rule, 4
        )
        if parser_cvss3_score or parser_cvss4_score:
            parser_severity = ""

        title = self.get_title(sarif_scanner, sarif_rule_id, sarif_rule)

        description = self.get_description(
            sarif_scanner=sarif_scanner,
            sarif_snippet=location.snippet,
            sarif_rule=sarif_rule,
            title=title,
            result=result,
        )

        sarif_cwe = None
        if sarif_rule.properties and isinstance(sarif_rule.properties, dict):
            sarif_cwe = self.get_cwe(sarif_rule.properties.get("tags", []))

        parser_vulnerability_id = self.get_dependency_check_vulnerability_id(
            sarif_scanner, title
        )

        origin_component_purl = self.get_dependency_check_origin_component_purl(
            sarif_scanner, sarif_location
        )
        if origin_component_purl:
            origin_component_name, origin_component_version = self.extract_component(
                origin_component_purl
            )
            location.uri = ""
        else:
            origin_component_name = ""
            origin_component_version = ""

        observation = Observation(
            parser_severity=parser_severity,
            title=title,
            description=description,
            origin_source_file=location.uri,
            origin_source_line_start=self.get_int_or_none(location.start_line),
            origin_source_line_end=self.get_int_or_none(location.end_line),
            scanner=sarif_scanner,
            cwe=sarif_cwe,
            cvss3_score=parser_cvss3_score,
            cvss3_vector=parser_cvss3_vector,
            cvss4_score=parser_cvss4_score,
            cvss4_vector=parser_cvss4_vector,
            vulnerability_id=parser_vulnerability_id,
            origin_component_purl=origin_component_purl,
            origin_component_name=origin_component_name,
            origin_component_version=origin_component_version,
        )

        evidence = []
        evidence.append("Rule")
        evidence.append(dumps(sarif_rule.rule_dict))
        observation.unsaved_evidences.append(evidence)

        evidence = []
        evidence.append("Result")
        evidence.append(dumps(result))
        observation.unsaved_evidences.append(evidence)

        observation.unsaved_references = []
        if sarif_rule.help_uri:
            observation.unsaved_references.append(sarif_rule.help_uri)

        observations.append(observation)

    def get_title(
        self, sarif_scanner: str, sarif_rule_id: str, sarif_rule: Rule
    ) -> str:
        if sarif_rule.name:
            title = sarif_rule.name
        else:
            title = sarif_rule_id

        title = self.get_trivy_title(title, sarif_scanner, sarif_rule)

        return title

    def get_trivy_title(self, title: str, sarif_scanner: str, sarif_rule: Rule) -> str:
        # Rule name and rule id of Trivy are not very descriptive
        if sarif_scanner.lower().startswith("trivy") and sarif_rule.short_description:
            title = sarif_rule.short_description
        return title

    def get_location_data(self, sarif_location: Optional[dict]) -> Location:
        location = Location()
        if sarif_location:
            location.uri = (
                sarif_location.get("physicalLocation", {})
                .get("artifactLocation", {})
                .get("uri", "")
            )
            location.start_line = (
                sarif_location.get("physicalLocation", {})
                .get("region", {})
                .get("startLine")
            )
            location.end_line = (
                sarif_location.get("physicalLocation", {})
                .get("region", {})
                .get("endLine")
            )
            location.snippet = (
                sarif_location.get("physicalLocation", {})
                .get("region", {})
                .get("snippet", {})
                .get("text")
            )

        return location

    def get_parser_severity(
        self, result: dict, sarif_scanner: str, sarif_rule: Rule
    ) -> str:
        sarif_level = result.get("level")
        if sarif_level:
            parser_severity = SEVERITIES.get(
                sarif_level.lower(), Severity.SEVERITY_UNKNOWN
            )
        elif sarif_rule.default_level:
            parser_severity = SEVERITIES.get(
                sarif_rule.default_level.lower(),
                Severity.SEVERITY_UNKNOWN,
            )
        elif self.get_bandit_severity(sarif_scanner, result):
            parser_severity = self.get_bandit_severity(sarif_scanner, result)
        else:
            parser_severity = Severity.SEVERITY_UNKNOWN

        return parser_severity

    def get_description(  # pylint: disable=too-many-branches
        self,
        *,
        sarif_scanner: str,
        sarif_snippet: Optional[str],
        sarif_rule: Rule,
        title: str,
        result: dict,
    ) -> str:
        description = ""

        sarif_message_text = result.get("message", {}).get("text")
        if sarif_message_text and not sarif_scanner.lower().startswith("trivy"):
            # Message text of Trivy has only redundant information
            description += f"{sarif_message_text}\n\n"

        if (
            sarif_rule.short_description
            and sarif_rule.short_description not in sarif_message_text
            and sarif_rule.short_description not in title
            and not sarif_scanner.lower().startswith("semgrep")
        ):
            # Rule short description of some scanners have only redundant information
            description += (
                f"**Rule short description:** {sarif_rule.short_description}\n\n"
            )

        rule_short_description = (
            sarif_rule.short_description if sarif_rule.short_description else ""
        )
        if (
            sarif_rule.full_description
            and sarif_rule.full_description not in sarif_message_text
            and sarif_rule.full_description not in rule_short_description
            and not sarif_scanner.lower().startswith("semgrep")
        ):
            # Rule short description of some scanners have only redundant information
            description += (
                f"**Rule full description:** {sarif_rule.full_description}\n\n"
            )

        if (  # pylint: disable=too-many-boolean-expressions
            sarif_rule.help
            and sarif_rule.help not in sarif_message_text
            and sarif_rule.help not in rule_short_description
            and not sarif_scanner.lower().startswith("trivy")
            and not sarif_scanner.lower().startswith("semgrep")
            and not sarif_scanner.lower().startswith("checkov")
        ):
            # Still pretty easy to understand
            # Help text of some scanners have only redundant information
            description += f"**Rule help:** {sarif_rule.help}\n\n"

        if sarif_snippet:
            # Newlines at the end of the description are removed
            while sarif_snippet.endswith("\n"):
                sarif_snippet = sarif_snippet[:-1]
            if "\n" in sarif_snippet:
                description += f"**Snippet:**\n\n```\n\n{sarif_snippet}\n```\n\n"
            else:
                description += f"**Snippet:** `{sarif_snippet}`\n\n"

        sarif_properties = result.get("properties", {})
        if sarif_properties and isinstance(sarif_properties, dict):
            for key in sarif_properties:
                value = sarif_properties[key]
                if value:
                    description += f"**{key.title()}:** {str(value)}\n\n"

        if sarif_rule.properties and isinstance(sarif_rule.properties, dict):
            for key in sarif_rule.properties:
                value = sarif_rule.properties[key]
                if value:
                    description += f"**{key.title()}:** {str(value)}\n\n"

        return description

    def extract_component(self, origin_component_purl: str) -> Tuple[str, str]:
        purl = PackageURL.from_string(origin_component_purl)
        namespace = purl.namespace
        name = purl.name
        if purl.version:
            version = purl.version
        else:
            version = ""
        if namespace:
            origin_component_name = f"{namespace}:{name}"
        else:
            origin_component_name = name
        origin_component_version = version

        return origin_component_name, origin_component_version

    def get_rules(self, run: dict) -> dict[str, Rule]:
        rules = {}

        sarif_rules = run.get("tool", {}).get("driver", {}).get("rules", [])
        for sarif_rule in sarif_rules:
            if sarif_rule.get("help", {}).get("text"):
                rule_help = sarif_rule.get("help", {}).get("text")
            else:
                rule_help = sarif_rule.get("help", {}).get("markdown")
            rule = Rule(
                default_level=sarif_rule.get("defaultConfiguration", {}).get("level"),
                short_description=sarif_rule.get("shortDescription", {}).get("text"),
                full_description=sarif_rule.get("fullDescription", {}).get("text"),
                help_uri=sarif_rule.get("helpUri"),
                help=rule_help,
                id=sarif_rule.get("id"),
                name=sarif_rule.get("name"),
                properties=sarif_rule.get("properties", {}),
                rule_dict=sarif_rule,
            )
            if rule.id:
                rules[rule.id] = rule

        return rules

    def get_cwe(self, tags: list[str]) -> Optional[int]:
        if tags:
            for tag in tags:
                if tag.startswith("CWE-") and ":" in tag:
                    tag_parts = tag.split(":")
                    return self.get_int_or_none(tag_parts[0][4:])
        return None

    def get_bandit_severity(self, sarif_scanner: str, result: dict) -> str:
        # Bandit SARIF has no level, but stores the severity in a property
        bandit_severity = result.get("properties", {}).get("issue_severity")
        if sarif_scanner.lower().startswith("bandit") and bandit_severity:
            return bandit_severity.title()

        return ""

    def get_dependency_check_cvss(
        self, sarif_scanner: str, sarif_rule: Rule, version: int
    ):
        # Dependency Check SARIF has no proper level, but stores the severity in a property
        if (
            sarif_scanner.lower().startswith("dependency-check")
            and sarif_rule.properties
            and isinstance(sarif_rule.properties, dict)
        ):
            return sarif_rule.properties.get(
                f"cvssv{version}_baseScore"
            ), sarif_rule.properties.get(f"cvssv{version}_vector")

        return None, None

    def get_dependency_check_vulnerability_id(
        self, sarif_scanner: str, title: str
    ) -> str:
        # Dependency Check sets the title with a vulnerability
        if sarif_scanner.lower().startswith("dependency-check") and (
            title.startswith("CVE-") or title.startswith("GHSA-")
        ):
            return title

        return ""

    def get_dependency_check_origin_component_purl(
        self, sarif_scanner: str, location: Optional[dict]
    ) -> str:
        if location:
            logicalLocations = location.get("logicalLocations")
            if (
                sarif_scanner.lower().startswith("dependency-check")
                and logicalLocations
            ):
                fully_qualified_name = logicalLocations[0].get("fullyQualifiedName")
                if fully_qualified_name and fully_qualified_name.startswith("pkg:"):
                    return fully_qualified_name

        return ""

    def result_is_suppressed(self, result: dict) -> bool:
        suppressions = result.get("suppressions", {})
        for suppression in suppressions:
            status = suppression.get("status")
            if not status or status == "accepted":
                return True

        return False
