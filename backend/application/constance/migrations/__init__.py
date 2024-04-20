from typing import TYPE_CHECKING

from django.utils.functional import LazyObject


class LazyConfig(LazyObject):
    def _setup(self):
        from application.commons.models import Settings

        self._wrapped = Settings.load()


if TYPE_CHECKING:
    from application.commons.models import Settings
settings: "Settings" = LazyConfig()  # type: ignore [assignment]
# LazyObject wraps the Settings model and returns the instance of the model when accessed.
