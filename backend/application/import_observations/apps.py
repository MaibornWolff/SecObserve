from django.apps import AppConfig


class UploadObservationsConfig(AppConfig):
    name = "application.import_observations"
    verbose_name = "Upload observations"

    def ready(self) -> None:
        # This forces the schema extension for DRF to be loaded
        import config.schema  # noqa F401 pylint: disable=import-outside-toplevel,unused-import
