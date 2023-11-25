from threading import current_thread
from typing import Optional

from django.http.request import HttpRequest

from application.access_control.models import User

_requests: dict[str, HttpRequest] = {}


def get_current_request() -> Optional[HttpRequest]:
    return _requests.get(current_thread().name)  # nosec B113
    #  This is not a HTTP request


def get_current_user() -> Optional[User]:
    request = get_current_request()
    if request:
        return request.user  # type: ignore[return-value]

    return None


class GlobalRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        _requests[current_thread().name] = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
