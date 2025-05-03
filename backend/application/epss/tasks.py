import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.epss.services.cvss_bt import import_cvss_bt
from application.epss.services.epss import epss_apply_observations, import_epss
from application.notifications.services.tasks import handle_task_exception

logger = logging.getLogger("secobserve.epss")


@db_periodic_task(
    crontab(
        minute=settings_static.background_epss_import_crontab_minute,
        hour=settings_static.background_epss_import_crontab_hour,
    )
)
@lock_task("import_epss")
def task_import_epss() -> None:
    logger.info("--- Import_EPSS and cvss-bt - start ---")

    try:
        import_epss()
        epss_apply_observations()
        import_cvss_bt()

    except Exception as e:
        handle_task_exception(e)

    logger.info("--- Import_EPSS and cvss-bt - finished ---")
