from typing import TYPE_CHECKING

from django.utils.functional import LazyObject


class LazyConfig(LazyObject):
    def _setup(self) -> None:
        from application.commons.models import (  # pylint: disable=import-outside-toplevel
            Settings,
        )

        # Can't be imported because module wouldn't be ready

        self._wrapped = Settings.load()


if TYPE_CHECKING:
    from application.commons.models import Settings
settings_static: "Settings" = LazyConfig()  # type: ignore [assignment]
# LazyObject wraps the Settings model and returns the instance of the model when accessed.
