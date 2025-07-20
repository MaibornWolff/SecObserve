import functools
import inspect
import logging
import sys
import traceback
from datetime import timedelta
from typing import Any, Callable

from django.utils import timezone
from huey.contrib.djhuey import lock_task

from application.background_tasks.models import Periodic_Task
from application.background_tasks.types import Status
from application.commons.services.log_message import format_log_message
from application.notifications.services.send_notifications import (
    send_task_exception_notification,
)

logger = logging.getLogger("secobserve.task")


def so_periodic_task(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @lock_task(name)
        def wrapper() -> None:
            logger.info("--- %s - start ---", name)

            periodic_task = Periodic_Task(
                task=name,
                start_time=timezone.now(),
                status=Status.STATUS_RUNNING,
            )
            periodic_task.save()

            try:
                message = func()

                periodic_task.status = Status.STATUS_SUCCESS
                periodic_task.duration = (timezone.now() - periodic_task.start_time) / timedelta(milliseconds=1)
                periodic_task.message = str(message) if message else ""
                periodic_task.save()
            except Exception as e:
                periodic_task.status = Status.STATUS_FAILURE
                periodic_task.duration = (timezone.now() - periodic_task.start_time) / timedelta(milliseconds=1)
                periodic_task.message = str(e)
                periodic_task.save()

                handle_periodic_task_exception(e)
                return

            logger.info("--- %s - finished ---", name)

        return wrapper

    return decorator


def handle_periodic_task_exception(e: Exception) -> None:
    data: dict[str, Any] = {}
    function = None

    if sys.exc_info() and len(sys.exc_info()) >= 2 and sys.exc_info()[2]:
        frames = inspect.getinnerframes(sys.exc_info()[2])  # type: ignore[arg-type]
        if frames and len(frames) >= 2:
            function = frames[1].function
            data["function"] = function

    logger.error(
        format_log_message(
            message="Error while executing periodic background task",
            data=data,
            exception=e,
            username=None,
        )
    )
    logger.error(traceback.format_exc())

    send_task_exception_notification(function=function, arguments=None, user=None, exception=e, product=None)
