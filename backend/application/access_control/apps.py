from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccessControlConfig(AppConfig):
    name = "application.access_control"
    verbose_name = _("Access Control")

    def ready(self) -> None:
        try:
            import application.access_control.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass
