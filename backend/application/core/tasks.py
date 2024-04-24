import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.commons.services.tasks import handle_task_exception
from application.core.services.housekeeping import delete_inactive_branches

logger = logging.getLogger("secobserve.core")


@db_periodic_task(
    crontab(
        minute=settings_static.branch_housekeeping_crontab_minutes,
        hour=settings_static.branch_housekeeping_crontab_hours,
    )
)
@lock_task("branch_housekeeping")
def task_branch_housekeeping() -> None:
    logger.info("--- Branch_housekeeping - start ---")

    try:
        delete_inactive_branches()
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- Branch_housekeeping - finished ---")
