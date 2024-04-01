from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from application.access_control.api.permissions import (
    check_object_permission,
    check_post_permission,
)
from application.access_control.services.authorization import get_highest_user_role
from application.access_control.services.roles_permissions import Permissions, Roles
from application.core.models import Product


class UserHasProductPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Product_View,
            Permissions.Product_Edit,
            Permissions.Product_Delete,
        )


class UserHasProductGroupPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Product_Group_View,
            Permissions.Product_Group_Edit,
            Permissions.Product_Group_Delete,
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
            _check_delete_owner(request, obj)

        return check_object_permission(
            request,
            obj,
            Permissions.Product_Member_View,
            Permissions.Product_Member_Edit,
            Permissions.Product_Member_Delete,
        )


class UserHasProductAuthorizationGroupMemberPermission(BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(
            request,
            Product,
            "product",
            Permissions.Product_Authorization_Group_Member_Create,
        )

    def has_object_permission(self, request, view, obj):
        if (
            request.method == "DELETE"
            and obj.role == Roles.Owner
            and not request.user.is_superuser
        ):
            _check_delete_owner(request, obj)

        return check_object_permission(
            request,
            obj,
            Permissions.Product_Authorization_Group_Member_View,
            Permissions.Product_Authorization_Group_Member_Edit,
            Permissions.Product_Authorization_Group_Member_Delete,
        )


def _check_delete_owner(request, obj) -> bool:
    if get_highest_user_role(obj.product, request.user) == Roles.Owner:
        return True

    raise ValidationError("You are not permitted to delete an Owner")


class UserHasBranchPermission(BasePermission):
    def has_permission(self, request, view):
        return check_post_permission(
            request, Product, "product", Permissions.Branch_Create
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Branch_View,
            Permissions.Branch_Edit,
            Permissions.Branch_Delete,
        )


class UserHasServicePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request,
            obj,
            Permissions.Service_View,
            None,
            Permissions.Service_Delete,
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
