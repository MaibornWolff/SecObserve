import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.commons.models import Settings
from application.licenses.services.license import import_licenses
from application.notifications.services.tasks import handle_task_exception

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
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- License import - finished ---")
