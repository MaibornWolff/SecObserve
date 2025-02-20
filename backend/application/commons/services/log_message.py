from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request
from rest_framework.response import Response

from application.access_control.models import User
from application.commons.services.functions import get_classname
from application.commons.services.global_request import (
    get_current_request,
    get_current_user,
)


def format_log_message(  # pylint: disable=too-many-branches
    # There are quite a lot of branches, but at least they are not nested too much
    message: str = None,
    data: dict = None,
    user: User = None,
    response: Response = None,
    exception: Exception = None,
) -> str:
    message_dict = {}
    if message:
        message_dict["message"] = message
    elif exception:
        message_dict["message"] = str(exception)
    else:
        message_dict["message"] = "No message given"

    if data:
        for key in data.keys():
            message_dict[f"data_{str(key)}"] = str(data[key])

    current_user = get_current_user()
    current_request = get_current_request()

    if user:
        message_dict["user"] = user.username
    elif current_user:
        if not isinstance(current_user, AnonymousUser):
            message_dict["user"] = current_user.username

    if current_request:
        if current_request.method:
            message_dict["request_method"] = current_request.method
        message_dict["request_path"] = current_request.get_full_path()
        message_dict["request_client_ip"] = __get_client_ip(current_request)

    if response:
        message_dict["response_status"] = str(response.status_code)

    if exception:
        if message:
            message_dict["exception_message"] = str(exception)
        message_dict["exception_class"] = get_classname(exception)

    return str(message_dict)


def __get_client_ip(request: Request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
