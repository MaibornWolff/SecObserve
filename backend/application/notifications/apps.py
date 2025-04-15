from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "application.notifications"
    verbose_name = "Notifications"

    def ready(self) -> None:
        try:
            import application.notifications.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
