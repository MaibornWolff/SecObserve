from django.apps import AppConfig


class OSVConfig(AppConfig):
    name = "application.osv"
    verbose_name = "OSV (Open Source Vulnerabilities)"

    def ready(self):
        try:
            import application.issue_tracker.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
