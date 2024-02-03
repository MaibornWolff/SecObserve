from dataclasses import dataclass
from json import dumps, load
from typing import Optional

from django.core.files.base import File

from application.core.models import Observation
from application.core.types import Severity
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Type


@dataclass
class Component:
    bom_ref: str
    name: str
    version: str
    type: str
    purl: str
    cpe: str
    json: dict[str, str]


@dataclass
class Metadata:
    scanner: str
    container_name: str
    container_tag: str
    container_digest: str
    file: str


class CycloneDXParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "CycloneDX"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_SCA

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], {}

        bom_format = data.get("bomFormat")
        if bom_format != "CycloneDX":
            return False, ["File is not a CycloneDX SBOM"], {}

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        components = self._get_components(data)
        metadata = self._get_metadata(data)
        observations = self._create_observations(data, components, metadata)

        return observations

    def _get_components(self, data: dict) -> dict[str, Component]:
        components = {}

        root_component = self._get_root_component(data)
        if root_component:
            components[root_component.bom_ref] = root_component

        sbom_components = data.get("components", [])
        for sbom_component in sbom_components:
            component = self._get_component(sbom_component)
            if component:
                components[component.bom_ref] = component

        return components

    def _get_root_component(self, data: dict) -> Optional[Component]:
        metadata_component = data.get("metadata", {}).get("component")
        if not metadata_component:
            return None

        return self._get_component(metadata_component)

    def _get_component(self, component_data: dict[str, str]) -> Optional[Component]:
        if not component_data.get("bom-ref"):
            return None

        return Component(
            bom_ref=component_data.get("bom-ref", ""),
            name=component_data.get("name", ""),
            version=component_data.get("version", ""),
            type=component_data.get("type", ""),
            purl=component_data.get("purl", ""),
            cpe=component_data.get("cpe", ""),
            json=component_data,
        )

    def _create_observations(  # pylint: disable=too-many-locals
        self, data: dict, components: dict[str, Component], metadata: Metadata
    ) -> list[Observation]:
        observations = []

        for vulnerability in data.get("vulnerabilities", []):
            vulnerability_id = vulnerability.get("id")
            cvss3_score, cvss3_vector = self._get_cvss3(vulnerability)
            severity = ""
            if not cvss3_score:
                severity = self._get_highest_severity(vulnerability)
            cwe = self._get_cwe(vulnerability)
            description = vulnerability.get("description")
            detail = vulnerability.get("detail")
            if detail:
                description += f"\n\n{detail}"
            recommendation = vulnerability.get("recommendation")
            for affected in vulnerability.get("affects", []):
                ref = affected.get("ref")
                if ref:
                    component = components.get(ref)
                    if component:
                        title = vulnerability_id

                        (
                            observation_component_dependencies,
                            translated_component_dependencies,
                        ) = self._get_component_dependencies(
                            data, components, component
                        )

                        observation = Observation(
                            title=title,
                            description=description,
                            recommendation=recommendation,
                            parser_severity=severity,
                            vulnerability_id=vulnerability_id,
                            origin_component_name=component.name,
                            origin_component_version=component.version,
                            origin_component_purl=component.purl,
                            origin_component_cpe=component.cpe,
                            origin_component_dependencies=observation_component_dependencies,
                            cvss3_score=cvss3_score,
                            cvss3_vector=cvss3_vector,
                            cwe=cwe,
                            scanner=metadata.scanner,
                            origin_docker_image_name=metadata.container_name,
                            origin_docker_image_tag=metadata.container_tag,
                            origin_docker_image_digest=metadata.container_digest,
                            origin_source_file=metadata.file,
                        )

                        self._add_references(vulnerability, observation)

                        self._add_evidences(
                            vulnerability,
                            component,
                            observation,
                            translated_component_dependencies,
                        )

                        observations.append(observation)

        return observations

    def _get_component_dependencies(self, data, components, component):
        component_dependencies: list[dict[str, str | list[str]]] = []
        self._filter_component_dependencies(
            component.bom_ref,
            data.get("dependencies", []),
            component_dependencies,
        )
        observation_component_dependencies = ""
        translated_component_dependencies = []
        if component_dependencies:
            translated_component_dependencies = self._translate_component_dependencies(
                component_dependencies, components
            )

            observation_component_dependencies = self._get_dependencies(
                "",
                f"{component.name}:{component.version}",
                translated_component_dependencies,
            )

        return observation_component_dependencies, translated_component_dependencies

    def _get_metadata(self, data: dict) -> Metadata:
        scanner = ""
        container_name = ""
        container_tag = ""
        container_digest = ""
        file = ""

        tools = data.get("metadata", {}).get("tools")
        if tools:
            if isinstance(tools, dict):
                components_or_services = tools.get("components", [])
                if not components_or_services:
                    components_or_services = tools.get("services", [])
                if components_or_services:
                    scanner = components_or_services[0].get("name", "")
                    version = components_or_services[0].get("version")
                    if version:
                        scanner += " / " + version
            if isinstance(tools, list):
                scanner = tools[0].get("name", "")
                version = tools[0].get("version")
                if version:
                    scanner += " / " + version

        component_type = data.get("metadata", {}).get("component", {}).get("type")
        component_name = data.get("metadata", {}).get("component", {}).get("name", "")
        component_version = (
            data.get("metadata", {}).get("component", {}).get("version", "")
        )
        if component_type == "container":
            container_name = component_name
            if component_version and component_version.startswith("sha256:"):
                container_digest = component_version
            elif component_version:
                container_tag = component_version
        if component_type == "file":
            file = component_name

        return Metadata(
            scanner=scanner,
            container_name=container_name,
            container_tag=container_tag,
            container_digest=container_digest,
            file=file,
        )

    def _get_cvss3(self, vulnerability):
        ratings = vulnerability.get("ratings", [])
        if ratings:
            cvss3_score = 0
            for rating in ratings:
                method = rating.get("method")
                if method and method.lower().startswith("cvssv3"):
                    current_cvss3_score = rating.get("score", 0)
                    if current_cvss3_score > cvss3_score:
                        cvss3_score = current_cvss3_score
                        cvss3_vector = rating.get("vector")
            if cvss3_score > 0:
                return cvss3_score, cvss3_vector
        return None, None

    def _get_highest_severity(self, vulnerability):
        current_severity = Severity.SEVERITY_UNKOWN
        current_numerical_severity = 999
        ratings = vulnerability.get("ratings", [])
        if ratings:
            for rating in ratings:
                severity = rating.get("severity", Severity.SEVERITY_UNKOWN).capitalize()
                numerical_severity = Severity.NUMERICAL_SEVERITIES.get(severity, 99)
                if numerical_severity < current_numerical_severity:
                    current_severity = severity
        return current_severity

    def _get_cwe(self, vulnerability):
        cwes = vulnerability.get("cwes", [])
        if len(cwes) >= 1:
            return cwes[0]

        return None

    def _add_references(self, vulnerability: dict, observation: Observation) -> None:
        advisories = vulnerability.get("advisories", [])
        if advisories:
            for advisory in advisories:
                observation.unsaved_references.append(advisory.get("url"))

    def _add_evidences(
        self,
        vulnerability: dict,
        component: Component,
        observation: Observation,
        translated_component_dependencies: list[dict],
    ):
        evidence = []
        evidence.append("Vulnerability")
        evidence.append(dumps(vulnerability))
        observation.unsaved_evidences.append(evidence)
        evidence = []
        evidence.append("Component")
        evidence.append(dumps(component.json))
        observation.unsaved_evidences.append(evidence)

        if translated_component_dependencies:
            evidence = []
            evidence.append("Dependencies")
            evidence.append(dumps(translated_component_dependencies))
            observation.unsaved_evidences.append(evidence)

    def _filter_component_dependencies(
        self,
        bom_ref: str,
        dependencies: list[dict[str, str | list[str]]],
        component_dependencies: list[dict[str, str | list[str]]],
    ) -> None:
        for dependency in dependencies:
            if dependency in component_dependencies:
                continue
            depends_on = dependency.get("dependsOn", [])
            if bom_ref in depends_on:
                component_dependencies.append(dependency)
                self._filter_component_dependencies(
                    str(dependency.get("ref")), dependencies, component_dependencies
                )

    def _translate_component_dependencies(
        self,
        component_dependencies: list[dict[str, str | list[str]]],
        components: dict[str, Component],
    ) -> list[dict]:
        translated_component_dependencies = []

        for component_dependency in component_dependencies:
            translated_component_dependency: dict[str, str | list[str]] = {}

            translated_component_dependency["ref"] = self._get_bom_ref_name_version(
                str(component_dependency.get("ref")), components
            )

            translated_component_dependencies_inner: list[str] = []
            for dependency in component_dependency.get("dependsOn", []):
                translated_component_dependencies_inner.append(
                    self._get_bom_ref_name_version(dependency, components)
                )
            translated_component_dependencies_inner.sort()
            translated_component_dependency["dependsOn"] = (
                translated_component_dependencies_inner
            )

            translated_component_dependencies.append(translated_component_dependency)

        return translated_component_dependencies

    def _get_bom_ref_name_version(
        self, bom_ref: str, components: dict[str, Component]
    ) -> str:
        component = components.get(bom_ref, None)
        if not component:
            return ""

        if component.version:
            component_name_version = f"{component.name}:{component.version}"
        else:
            component_name_version = component.name

        return component_name_version

    def _get_dependencies(
        self,
        dependencies: str,
        component_version: str,
        translated_component_dependencies: list[dict],
    ) -> str:
        for dependency in translated_component_dependencies:
            ref = dependency.get("ref")
            depends_on = dependency.get("dependsOn", [])
            if (
                ref
                and ref != component_version
                and component_version in depends_on
                and (not dependencies or ref not in dependencies)
            ):
                if not dependencies:
                    dependencies = f"{ref} --> {component_version}"
                else:
                    dependencies = f"{ref} --> {dependencies}"

                dependencies = self._get_dependencies(
                    dependencies, ref, translated_component_dependencies
                )
                break

        return dependencies

    # def _get_dependencies(
    #     self,
    #     dependencies: list[str],
    #     list_pointer: int,
    #     component_version: str,
    #     translated_component_dependencies: dict,
    # ) -> None:
    #     i = -1
    #     current_dependency = None
    #     if dependencies:
    #         current_dependency = dependencies[list_pointer]
    #     for dependency in translated_component_dependencies:
    #         ref = dependency.get("ref")
    #         depends_on = dependency.get("dependsOn", [])
    #         if (
    #             ref
    #             and ref != component_version
    #             and component_version in depends_on
    #             and (not dependencies or not ref in dependencies[list_pointer])
    #         ):
    #             i += 1

    #             if len(dependencies) <= i:
    #                 if not dependencies or not current_dependency:
    #                     dependencies.append(f"{ref} --> {component_version}")
    #                 else:
    #                     dependencies.append(f"{ref} --> {current_dependency}")
    #                 list_pointer = i
    #             else:
    #                 dependencies[
    #                     list_pointer
    #                 ] = f"{ref} --> {dependencies[list_pointer]}"

    #             self._get_dependencies(
    #                 dependencies, list_pointer, ref, translated_component_dependencies
    #             )
