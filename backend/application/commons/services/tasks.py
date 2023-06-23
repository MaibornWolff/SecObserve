import inspect
import logging
import traceback
from typing import Any

from application.access_control.models import User
from application.commons.models import Notification
from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.tasks")


def handle_task_exception(e: Exception, user: User) -> None:
    data: dict[str, Any] = {}

    current_frame = inspect.currentframe()
    if current_frame:
        frame = current_frame.f_back
        if frame:
            args, _, _, values = inspect.getargvalues(frame)
            arguments = {}
            for arg in args:
                arguments[arg] = values[arg]

            data["function"] = frame.f_code.co_name
            data["arguments"] = arguments

    logger.error(
        format_log_message(
            message="Error while executing background task",
            data=data,
            exception=e,
            user=user,
        )
    )
    logger.error(traceback.format_exc())

    observation = data.get("arguments", {}).get("observation")
    product = None
    if observation:
        product = observation.product

    Notification.objects.create(
        name="Error in background task",
        message=str(e),
        function=data.get("function"),
        arguments=data.get("arguments"),
        product=product,
        observation=observation,
        user=user,
    )
