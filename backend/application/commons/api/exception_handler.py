import logging
import traceback
from typing import Optional

from django.db.models.deletion import ProtectedError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import exception_handler

from application.commons.services.log_message import format_log_message
from application.commons.services.push_notifications import send_exception_notification

logger = logging.getLogger("secobserve.exception_handler")


def custom_exception_handler(exc, context):
    response: Optional[Response]
    if isinstance(exc, ProtectedError):
        # An object cannot be deleted because it has dependent objects.
        response = Response()
        response.status_code = HTTP_409_CONFLICT
        response.data = {}
        response.data["message"] = format_exception_message(exc)
    else:
        # Call REST framework's default exception handler first,
        # to get the standard error response.
        response = exception_handler(exc, context)

        if response is None:
            # There is no standard error response, so we assume an unexpected
            # exception. It is logged but no details are given to the user,
            # to avoid leaking internal technical information.
            response = Response()
            response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
            response.data = {}
            response.data["message"] = "Internal server error, check logs for details"
            logger.error(format_log_message(response=response, exception=exc))
            logger.error(traceback.format_exc())
            send_exception_notification(exc)
        else:
            if response.status_code < 500:
                if response.status_code in (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN):
                    logger.warning(format_log_message(response=response, exception=exc))

                # HTTP status codes lower than 500 are no technical errors.
                # They need not to be logged and we provide the exception
                # message in the response.
                response.data = {}
                response.data["message"] = format_exception_message(exc)
            else:
                # HTTP status code 500 or higher are technical errors.
                # They get logged but no details are given to the user,
                # to avoid leaking internal technical information.
                logger.error(format_log_message(response=response, exception=exc))
                logger.error(traceback.format_exc())
                send_exception_notification(exc)
                response.data = {}
                response.data[
                    "message"
                ] = "Internal server error, check logs for details"

    return response


def format_exception_message(exc):
    if (
        hasattr(exc, "detail")
        and exc.detail
        and type(exc.detail).__name__ == "ReturnDict"
    ):
        message_list = []
        for key in exc.detail:
            for message in exc.detail.get(key):
                message_list.append(
                    f'{key.replace("_", " ").capitalize()}: {str(message)}'
                )
        return "\n".join(message_list)

    if (
        hasattr(exc, "detail")
        and exc.detail
        and isinstance(exc.detail, list)
        and len(exc.detail) > 0
    ):
        return " / ".join(exc.detail)

    if hasattr(exc, "args") and exc.args and "protected foreign keys" in exc.args[0]:
        return exc.args[0].split("protected foreign keys")[0] + "protected foreign keys"

    return str(exc)
