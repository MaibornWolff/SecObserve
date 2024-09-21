from rest_framework.permissions import BasePermission

from application.access_control.api.permissions_base import check_object_permission
from application.access_control.services.roles_permissions import Permissions


class UserHasVEXPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request=request,
            object_to_check=obj,
            get_permission=Permissions.VEX_View,
            put_permission=Permissions.VEX_Edit,
            delete_permission=Permissions.VEX_Delete,
        )


class UserHasVEXCounterPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        return request.user and request.user.is_superuser
