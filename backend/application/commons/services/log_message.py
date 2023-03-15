from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response

from application.access_control.models import User
from application.commons.services.global_request import (
    get_current_request,
    get_current_user,
)


def format_log_message(
    message: str = None,
    data: dict = None,
    user: User = None,
    response: Response = None,
    exception: Exception = None,
) -> str:
    message_dict = dict()
    if message:
        message_dict["message"] = message
    elif exception:
        message_dict["message"] = str(exception)
    else:
        message_dict["message"] = "No message given"

    if data:
        for key in data.keys():
            message_dict[f"data_{str(key)}"] = str(data[key])

    if user:
        message_dict["user"] = user.username
    elif get_current_user():
        if not isinstance(get_current_user(), AnonymousUser):
            message_dict["user"] = get_current_user().username

    if get_current_request():
        message_dict["request_method"] = get_current_request().method
        message_dict["request_path"] = get_current_request().get_full_path()
        message_dict["request_client_ip"] = __get_client_ip(get_current_request())

    if response:
        message_dict["response_status"] = response.status_code

    if exception:
        if message:
            message_dict["exception_message"] = str(exception)
        message_dict["exception_class"] = __get_classname(exception)

    return str(message_dict)


def __get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def __get_classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name
