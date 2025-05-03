from django.apps import AppConfig


class EPSSConfig(AppConfig):
    name = "application.epss"
    verbose_name = "EPSS"

    def ready(self) -> None:
        try:
            import application.epss.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
