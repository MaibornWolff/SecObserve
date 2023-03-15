from rest_framework.permissions import BasePermission

from application.access_control.api.permissions import (
    check_post_permission,
    check_object_permission,
)
from application.access_control.services.roles_permissions import Permissions, Roles
from application.core.models import Product, Observation
from application.core.queries.product import get_product_member


class UserHasProductPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Product_View,
            Permissions.Product_Edit,
            Permissions.Product_Delete,
        )


class UserHasProductMemberPermission(BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(
            request, Product, "product", Permissions.Product_Member_Create
        )

    def has_object_permission(self, request, view, obj):
        if (
            request.method == "DELETE"
            and obj.role == Roles.Owner
            and not request.user.is_superuser
        ):
            # Only superusers and Owners are allowed to delete Owners
            own_product_member = get_product_member(obj.product, request.user)
            if not own_product_member or not own_product_member.role == Roles.Owner:
                return False

        return check_object_permission(
            request,
            obj,
            Permissions.Product_Member_View,
            Permissions.Product_Member_Edit,
            Permissions.Product_Member_Delete,
        )


class UserHasObservationPermission(BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(
            request, Product, "product", Permissions.Observation_Create
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Observation_View,
            Permissions.Observation_Edit,
            Permissions.Observation_Delete,
        )


class UserHasEvidencePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Observation_View,
            None,
            None,
        )
