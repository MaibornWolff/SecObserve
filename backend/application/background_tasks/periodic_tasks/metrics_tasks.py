from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from application.background_tasks.services.task_base import so_periodic_task
from application.commons import settings_static
from application.metrics.services.metrics import calculate_product_metrics


@db_periodic_task(crontab(minute=f"*/{settings_static.background_product_metrics_interval_minutes}"))
@so_periodic_task("Calculate product metrics")
def task_calculate_product_metrics() -> None:
    calculate_product_metrics()
