from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "application.core"
    verbose_name = "Core"

    def ready(self):
        try:
            import application.core.signals  # noqa F401
        except ImportError:
            pass

        import config.schema  # noqa: F401
