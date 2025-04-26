from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class UserHasSuperuserPermission(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        return request.user.is_superuser

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_superuser
