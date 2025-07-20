from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from application.background_tasks.services.task_base import so_periodic_task
from application.commons import settings_static
from application.core.services.housekeeping import (
    delete_inactive_branches_and_set_flags,
)
from application.core.services.risk_acceptance_expiry_task import (
    expire_risk_acceptances,
)


@db_periodic_task(
    crontab(
        minute=settings_static.branch_housekeeping_crontab_minute,
        hour=settings_static.branch_housekeeping_crontab_hour,
    )
)
@so_periodic_task("Branch housekeeping")
def task_branch_housekeeping() -> None:
    delete_inactive_branches_and_set_flags()


@db_periodic_task(
    crontab(
        minute=settings_static.risk_acceptance_expiry_crontab_minute,
        hour=settings_static.risk_acceptance_expiry_crontab_hour,
    )
)
@so_periodic_task("Expire risk acceptances")
def task_expire_risk_acceptances() -> None:
    expire_risk_acceptances()
