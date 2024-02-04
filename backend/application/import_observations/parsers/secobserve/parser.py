from json import load

from django.core.files.base import File

from application.core.models import Observation
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Type


class SecObserveParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "SecObserve"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_OTHER

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], {}

        if not data.get("format") == "SecObserve":
            return False, ["File is not a SecObserve format"], {}

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        observations = []

        for uploaded_observation in data.get("observations", []):
            observation = Observation(
                title=uploaded_observation.get("title"),
                description=uploaded_observation.get("description"),
                recommendation=uploaded_observation.get("recommendation"),
                parser_severity=uploaded_observation.get("parser_severity"),
                scanner_observation_id=uploaded_observation.get(
                    "scanner_observation_id"
                ),
                vulnerability_id=uploaded_observation.get("vulnerability_id"),
                origin_component_name=uploaded_observation.get("origin_component_name"),
                origin_component_version=uploaded_observation.get(
                    "origin_component_version"
                ),
                origin_component_name_version=uploaded_observation.get(
                    "origin_component_name_version"
                ),
                origin_component_purl=uploaded_observation.get("origin_component_purl"),
                origin_component_cpe=uploaded_observation.get("origin_component_cpe"),
                origin_docker_image_name=uploaded_observation.get(
                    "origin_docker_image_name"
                ),
                origin_docker_image_tag=uploaded_observation.get(
                    "origin_docker_image_tag"
                ),
                origin_docker_image_name_tag=uploaded_observation.get(
                    "origin_docker_image_name_tag"
                ),
                origin_endpoint_url=uploaded_observation.get("origin_endpoint_url"),
                origin_service_name=uploaded_observation.get("origin_service_name"),
                origin_source_file=uploaded_observation.get("origin_source_file"),
                origin_source_line_start=uploaded_observation.get(
                    "origin_source_line_start"
                ),
                origin_source_line_end=uploaded_observation.get(
                    "origin_source_line_end"
                ),
                cvss3_score=uploaded_observation.get("cvss3_score"),
                cvss3_vector=uploaded_observation.get("cvss3_vector"),
                cwe=uploaded_observation.get("cwe"),
                scanner=uploaded_observation.get("scanner"),
            )
            reference = uploaded_observation.get("reference")
            if reference:
                observation.unsaved_references = [reference]
            observations.append(observation)
        return observations
