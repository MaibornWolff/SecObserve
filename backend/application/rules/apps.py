from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RulesConfig(AppConfig):
    name = "application.rules"
    verbose_name = _("Rules")

    def ready(self):
        try:
            import application.rules.signals  # noqa F401
        except ImportError:
            pass
