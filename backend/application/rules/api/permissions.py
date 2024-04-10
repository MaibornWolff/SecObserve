from rest_framework.permissions import BasePermission

from application.access_control.api.permissions_base import (
    check_object_permission,
    check_post_permission,
)
from application.access_control.services.roles_permissions import Permissions
from application.core.models import Product


class UserHasGeneralRulePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        return request.user and request.user.is_superuser


class UserHasProductRulePermission(BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(
            request, Product, "product", Permissions.Product_Rule_Create
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Product_Rule_View,
            Permissions.Product_Rule_Edit,
            Permissions.Product_Rule_Delete,
        )
