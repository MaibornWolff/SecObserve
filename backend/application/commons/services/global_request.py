from threading import current_thread
from django.http.request import HttpRequest
from application.access_control.models import User

_requests = {}


def get_current_request() -> HttpRequest:
    return _requests.get(current_thread().name)


def get_current_user() -> User:
    request = get_current_request()
    if request:
        return request.user
    else:
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
