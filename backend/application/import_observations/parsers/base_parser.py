from typing import Any, Optional

from application.core.models import Observation
from application.import_observations.models import Api_Configuration
from application.licenses.models import License_Component


class BaseParser:
    @classmethod
    def get_name(cls) -> str:
        raise NotImplementedError("get_name() must be overridden")

    @classmethod
    def get_type(cls) -> str:
        raise NotImplementedError("get_type() must be overridden")

    def get_observations(self, data: Any) -> list[Observation]:
        raise NotImplementedError("get_observations() must be overridden")

    def get_license_components(
        self, data: Any  # pylint: disable=unused-argument
    ) -> list[License_Component]:
        # data is used in the child classes
        return []

    def get_int_or_none(self, value: Optional[str]) -> int | None:
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
    @classmethod
    def get_filetype(cls) -> str:
        raise NotImplementedError("check_format() must be overridden")

    def check_format(self, data: Any) -> bool:
        raise NotImplementedError("check_format() must be overridden")
