import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.commons.services.tasks import handle_task_exception
from application.metrics.services.metrics import calculate_product_metrics

logger = logging.getLogger("secobserve.metrics")


@db_periodic_task(crontab(minute=f"*/{settings_static.background_product_metrics_interval_minutes}"))
@lock_task("calculate_product_metrics")
def task_calculate_product_metrics() -> None:
    logger.info("--- Calculate_product_metrics - start ---")

    try:
        calculate_product_metrics()
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- Calculate_product_metrics - finished ---")
