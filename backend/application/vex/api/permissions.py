from rest_framework.permissions import BasePermission

from application.access_control.api.permissions import check_object_permission
from application.access_control.services.roles_permissions import Permissions


class UserHasVEXPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.VEX_View,
            Permissions.VEX_Edit,
            Permissions.VEX_Delete,
        )


class UserHasVEXCounterPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        return request.user and request.user.is_superuser
