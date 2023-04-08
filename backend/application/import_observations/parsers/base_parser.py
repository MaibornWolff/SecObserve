from typing import Any

from django.core.files.base import File

from application.core.models import Observation
from application.import_observations.models import Api_Configuration


class BaseParser:
    @classmethod
    def get_name(cls) -> str:
        raise NotImplementedError("get_name() must be overridden")

    @classmethod
    def get_type(cls) -> str:
        raise NotImplementedError("get_type() must be overridden")

    def get_observations(self, data: Any) -> list[Observation]:
        raise NotImplementedError("get_observations() must be overridden")

    def get_int_or_none(self, value: str) -> int | None:
        if value:
            try:
                return int(value)
            except Exception:
                return None
        else:
            return None


class BaseAPIParser:
    def check_connection(
        self, api_configuration: Api_Configuration
    ) -> tuple[bool, list[str], dict | list]:
        raise NotImplementedError("check_connection() must be overridden")


class BaseFileParser:
    def check_format(self, file: File) -> tuple[bool, list[str], dict | list]:
        raise NotImplementedError("check_format() must be overridden")
