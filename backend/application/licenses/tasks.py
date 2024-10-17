import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.commons.models import Settings
from application.commons.services.tasks import handle_task_exception
from application.licenses.services.licenses import (
    import_license_groups,
    import_licenses,
)

logger = logging.getLogger("secobserve.import_licenses")


@db_periodic_task(
    crontab(
        minute=settings_static.license_import_crontab_minute,
        hour=settings_static.license_import_crontab_hour,
    )
)
@lock_task("license_import")
def task_api_import() -> None:
    settings = Settings.load()
    if not settings.feature_license_management:
        return

    logger.info("--- License import - start ---")

    try:
        import_licenses()
        import_license_groups()
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- License import - finished ---")
