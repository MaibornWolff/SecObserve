from threading import current_thread
from typing import Any, Optional

from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request
from rest_framework.response import Response

from application.access_control.models import User

_requests: dict[str, Request] = {}


def get_current_request() -> Optional[Request]:
    return _requests.get(current_thread().name)


def get_current_user() -> Optional[User]:
    request = get_current_request()
    if request and request.user and not isinstance(request.user, AnonymousUser):
        return request.user

    return None


class GlobalRequestMiddleware:
    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: Request) -> Response:
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        _requests[current_thread().name] = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
