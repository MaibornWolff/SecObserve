import logging

from constance import config
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons.services.tasks import handle_task_exception
from application.epss.services.epss import epss_apply_observations, import_epss

logger = logging.getLogger("secobserve.epss")


@db_periodic_task(
    crontab(
        minute=config.BACKGROUND_EPSS_IMPORT_CRONTAB_MINUTES,
        hour=config.BACKGROUND_EPSS_IMPORT_CRONTAB_HOURS,
    )
)
@lock_task("import_epss")
def task_import_epss() -> None:
    logger.info("--- Import_EPSS - start ---")

    try:
        import_epss()
        num_updated = epss_apply_observations()
        logger.info("Updated %d observations with EPSS scores", num_updated)
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- Import_EPSS - finished ---")
