import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.commons.services.tasks import handle_task_exception

logger = logging.getLogger("secobserve.import_observations")


@db_periodic_task(
    crontab(
        minute=settings_static.api_import_crontab_minute,
        hour=settings_static.api_import_crontab_hour,
    )
)
@lock_task("api_import")
def task_api_import() -> None:
    logger.info("--- API import - start ---")

    try:
        pass
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- API import - finished ---")
