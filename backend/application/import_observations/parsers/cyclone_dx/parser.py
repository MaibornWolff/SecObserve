from json import load, dumps
from django.core.files.base import File

from application.core.models import Observation, Parser
from application.import_observations.parsers.base_parser import (
    BaseParser,
    BaseFileParser,
)


class Component:
    def __init__(self, name, version, type, purl, cpe, json):
        self.name = name
        self.version = version
        self.type = type
        self.purl = purl
        self.cpe = cpe
        self.json = json


class Metadata:
    def __init__(self, scanner, container, file):
        self.scanner = scanner
        self.container = container
        self.file = file


class CycloneDXParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "CycloneDX"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_SCA

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], {}

        bom_format = data.get("bomFormat")
        if bom_format != "CycloneDX":
            return False, ["Data is not a CycloneDX SBOM"], {}

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        components = self.get_components(data)
        metadata = self.get_metadata(data)
        observations = self.create_observations(data, components, metadata)

        return observations

    def get_components(self, data: dict) -> dict[str, Component]:
        components = {}
        metadata_component = data.get("metadata", {}).get("component")
        if metadata_component:
            bom_ref = metadata_component.get("bom-ref")
            if bom_ref:
                component = Component(
                    name=metadata_component.get("name"),
                    version=metadata_component.get("version"),
                    type=metadata_component.get("type"),
                    purl=metadata_component.get("purl"),
                    cpe=metadata_component.get("cpe"),
                    json=metadata_component,
                )
                components[bom_ref] = component
        sbom_components = data.get("components", [])
        for sbom_component in sbom_components:
            bom_ref = sbom_component.get("bom-ref")
            if bom_ref:
                component = Component(
                    name=sbom_component.get("name"),
                    version=sbom_component.get("version"),
                    type=sbom_component.get("type"),
                    purl=sbom_component.get("purl"),
                    cpe=sbom_component.get("cpe"),
                    json=sbom_component,
                )
                components[bom_ref] = component
        return components

    def create_observations(
        self, data: dict, components: dict[str, Component], metadata: Metadata
    ) -> list[Observation]:
        observations = []

        vulnerabilities = data.get("vulnerabilities", [])
        for vulnerability in vulnerabilities:
            id = vulnerability.get("id")
            cvss3_score, cvss3_vector = self.get_cvss3(vulnerability)
            severity = Observation.SEVERITY_UNKOWN
            if not cvss3_score:
                severity = self.get_highest_severity(vulnerability)
            cwe = self.get_cwe(vulnerability)
            description = vulnerability.get("description")
            detail = vulnerability.get("detail")
            if detail:
                description += f"\n\n{detail}"
            recommendation = vulnerability.get("recommendation")
            advisories = vulnerability.get("advisories", [])
            affects = vulnerability.get("affects", [])
            for affected in affects:
                ref = affected.get("ref")
                if ref:
                    component = components.get(ref)
                    if component:
                        title = id
                        observation = Observation(
                            title=title,
                            description=description,
                            recommendation=recommendation,
                            parser_severity=severity,
                            vulnerability_id=id,
                            origin_component_name=component.name,
                            origin_component_version=component.version,
                            origin_component_purl=component.purl,
                            origin_component_cpe=component.cpe,
                            cvss3_score=cvss3_score,
                            cvss3_vector=cvss3_vector,
                            cwe=cwe,
                            scanner=metadata.scanner,
                            origin_docker_image_name_tag=metadata.container,
                            origin_source_file=metadata.file,
                        )

                        if advisories:
                            for advisory in advisories:
                                observation.unsaved_references.append(
                                    advisory.get("url")
                                )

                        evidence = []
                        evidence.append("Vulnerability")
                        evidence.append(dumps(vulnerability))
                        observation.unsaved_evidences.append(evidence)
                        evidence = []
                        evidence.append("Component")
                        evidence.append(dumps(component.json))
                        observation.unsaved_evidences.append(evidence)

                        observations.append(observation)

        return observations

    def get_metadata(self, data: dict) -> Metadata:
        scanner = None
        container = None
        file = None

        tools = data.get("metadata", {}).get("tools", [])
        if len(tools) >= 1:
            scanner = tools[0].get("name")
            version = tools[0].get("version")
            if version:
                scanner += " / " + version

        type = data.get("metadata", {}).get("component", {}).get("type")
        name = data.get("metadata", {}).get("component", {}).get("name")
        if type == "container":
            container = name
        if type == "file":
            file = name

        return Metadata(scanner, container, file)

    def get_cvss3(self, vulnerability):
        ratings = vulnerability.get("ratings", [])
        if ratings:
            for rating in ratings:
                method = rating.get("method")
                if method and method.lower().startswith("cvssv3"):
                    cvss3_score = rating.get("score")
                    cvss3_vector = rating.get("vector")
                    return cvss3_score, cvss3_vector
        return None, None

    def get_highest_severity(self, vulnerability):
        current_severity = None
        current_numerical_severity = 999
        ratings = vulnerability.get("ratings", [])
        if ratings:
            for rating in ratings:
                severity = rating.get(
                    "severity", Observation.SEVERITY_UNKOWN
                ).capitalize()
                numerical_severity = Observation.NUMERICAL_SEVERITIES.get(severity, 99)
                if numerical_severity < current_numerical_severity:
                    current_severity = severity
        return current_severity

    def get_cwe(self, vulnerability):
        cwes = vulnerability.get("cwes", [])
        if len(cwes) >= 1:
            return cwes[0]
