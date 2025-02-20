from django.apps import AppConfig


class LicenseConfig(AppConfig):
    name = "application.licenses"
    verbose_name = "Licenses"

    def ready(self) -> None:
        try:
            import application.licenses.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
