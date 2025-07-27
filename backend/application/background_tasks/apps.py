from django.apps import AppConfig


class BackgroundTasksConfig(AppConfig):
    name = "application.background_tasks"
    verbose_name = "Background tasks"

    def ready(self) -> None:
        try:
            import application.background_tasks.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
