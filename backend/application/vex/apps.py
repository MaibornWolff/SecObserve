from django.apps import AppConfig


class VEXConfig(AppConfig):
    name = "application.vex"
    verbose_name = "Vulnerability Exploitability eXchange"

    def ready(self) -> None:
        try:
            import application.vex.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
