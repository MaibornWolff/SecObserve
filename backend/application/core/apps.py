from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "application.core"
    verbose_name = "Core"

    def ready(self) -> None:
        try:
            import application.core.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
