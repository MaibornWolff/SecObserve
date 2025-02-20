from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "application.issue_tracker"
    verbose_name = "Issue Tracker"

    def ready(self) -> None:
        try:
            import application.issue_tracker.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
