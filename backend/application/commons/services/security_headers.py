from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response

# see https://adamj.eu/tech/2021/05/01/how-to-set-coep-coop-corp-security-headers-in-django/


class SecurityHeadersMiddleware:
    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        response = self.get_response(request)
        response["Cross-Origin-Embedder-Policy"] = "require-corp"
        response["Cross-Origin-Opener-Policy"] = "same-origin"
        response["Cross-Origin-Resource-Policy"] = "same-site"
        response["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
        response["Permissions-Policy"] = "geolocation=() camera=(), microphone=()"
        return response
