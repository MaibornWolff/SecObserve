from rest_framework.permissions import BasePermission

from application.access_control.api.permissions import check_object_permission
from application.access_control.services.roles_permissions import Permissions


class UserHasNotificationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.product:
            return check_object_permission(
                request,
                obj.product,
                Permissions.Product_View,
                None,
                Permissions.Product_Delete,
            )

        if request.user and request.user.is_superuser:
            return True

        return False
