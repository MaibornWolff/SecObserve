from dataclasses import dataclass
from json import dumps, load
from typing import Any

from django.core.files.base import File
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.model.relationship import RelationshipType
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.json_like_dict_parser import JsonLikeDictParser

from application.core.models import Observation
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Type
from application.licenses.models import License_Component


@dataclass
class ImportedData:
    data_json: dict
    document: Document


class SPDXParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "SPDX"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_SCA

    def check_format(self, file: File) -> tuple[bool, list[str], Any]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], {}

        try:
            document = JsonLikeDictParser().parse(data)
        except SPDXParsingError as e:
            return False, e.get_messages(), {}

        imported_data = ImportedData(data, document)

        return True, [], imported_data

    def get_observations(self, data: ImportedData) -> list[Observation]:
        return []

    def get_license_components(self, data: ImportedData) -> list[License_Component]:
        observations = []

        packages = self._create_package_dict(data.data_json)
        relationships = self._create_relationship_dict(data.document, packages)

        for package in data.document.packages:
            version = ""
            if package.version is not None:
                version = str(package.version)

            unsaved_license = None
            if (
                package.license_concluded is not None
                and str(package.license_concluded) != ""
                and str(package.license_concluded) != "NOASSERTION"
            ):
                unsaved_license = package.license_concluded
            elif (
                package.license_declared is not None
                and str(package.license_declared) != ""
                and str(package.license_declared) != "NOASSERTION"
            ):
                unsaved_license = package.license_declared

            purl = ""
            for external_reference in package.external_references:
                if external_reference.reference_type == "purl":
                    purl = external_reference.locator
                    break

            dependencies = self._get_dependencies(
                package.spdx_id, packages, relationships
            )

            license_component = License_Component(
                name=package.name,
                version=version,
                purl=purl,
                dependencies=dependencies,
            )
            if unsaved_license is not None:
                license_component.unsaved_license = str(unsaved_license)

            evidence = []
            package_json = packages.get(package.spdx_id)
            if package_json:
                evidence.append("Package")
                evidence.append(dumps(package_json))
                license_component.unsaved_evidences.append(evidence)

            observations.append(license_component)

        return observations

    def _create_package_dict(self, data: dict) -> dict[str, dict]:
        package_dict = {}
        for package in data["packages"]:
            package_dict[package["SPDXID"]] = package
        return package_dict

    def _create_relationship_dict(
        self, document: Document, package_dict: dict[str, dict]
    ) -> dict[str, list[str]]:
        relationship_dict: dict[str, list[str]] = {}
        for relationship in document.relationships:
            if (
                relationship.spdx_element_id in package_dict.keys()
                and relationship.related_spdx_element_id in package_dict.keys()
                and (
                    relationship.relationship_type
                    in (RelationshipType.DEPENDS_ON, RelationshipType.CONTAINS)
                )
            ):
                relationship_value = relationship_dict.get(
                    str(relationship.related_spdx_element_id), []
                )
                relationship_value.append(relationship.spdx_element_id)
                relationship_dict[str(relationship.related_spdx_element_id)] = (
                    relationship_value
                )
        return relationship_dict

    def _get_dependencies(
        self, package_id: str, package_dict: dict, relationship_dict: dict
    ) -> str:
        dependencies: list[str] = []
        self._get_dependencies_recursive(
            package_id, package_dict, relationship_dict, dependencies
        )

        dependencies.sort()
        return "\n".join(dependencies)

    def _get_dependencies_recursive(
        self,
        package_id: str,
        package_dict: dict,
        relationship_dict: dict,
        dependencies: list,
    ) -> None:
        if package_id in relationship_dict.keys():
            for dependency_id in relationship_dict[package_id]:
                translated_dependency_id = self._translate_package_id(
                    dependency_id, package_dict
                )
                translated_package_id = self._translate_package_id(
                    package_id, package_dict
                )
                dependency = f"{translated_dependency_id} --> {translated_package_id}"
                if dependency not in dependencies:
                    dependencies.append(dependency)
                    self._get_dependencies_recursive(
                        dependency_id, package_dict, relationship_dict, dependencies
                    )

    def _translate_package_id(self, package_id: str, package_dict: dict) -> str:
        package = package_dict.get(package_id)
        if not package:
            return ""

        if package.get("versionInfo"):
            return f"{package.get('name', '')}:{package.get('versionInfo', '')}"

        return package.get("name", "")
