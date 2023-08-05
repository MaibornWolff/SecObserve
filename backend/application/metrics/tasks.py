import logging

from constance import config
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons.services.tasks import handle_task_exception
from application.metrics.services.metrics import calculate_product_metrics

logger = logging.getLogger("secobserve.metrics")


@db_periodic_task(
    crontab(minute=f"*/{config.BACKGROUND_PRODUCT_METRICS_INTERVAL_MINUTES}")
)
@lock_task("calculate_product_metrics")
def task_calculate_product_metrics() -> None:
    logger.info("--- Calculate_product_metrics - start ---")

    try:
        calculate_product_metrics()
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- Calculate_product_metrics - finished ---")
