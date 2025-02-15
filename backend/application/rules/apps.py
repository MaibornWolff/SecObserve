from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RulesConfig(AppConfig):
    name = "application.rules"
    verbose_name = _("Rules")

    def ready(self) -> None:
        try:
            import application.rules.signals  # noqa F401 pylint: disable=import-outside-toplevel,unused-import
        except ImportError:
            pass
