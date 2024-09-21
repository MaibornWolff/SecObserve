from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from application.access_control.api.permissions_base import (
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
            request=request,
            object_to_check=obj,
            get_permission=Permissions.Product_View,
            put_permission=Permissions.Product_Edit,
            delete_permission=Permissions.Product_Delete,
        )


class UserHasProductGroupPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request=request,
            object_to_check=obj,
            get_permission=Permissions.Product_Group_View,
            put_permission=Permissions.Product_Group_Edit,
            delete_permission=Permissions.Product_Group_Delete,
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
            request=request,
            object_to_check=obj,
            get_permission=Permissions.Product_Member_View,
            put_permission=Permissions.Product_Member_Edit,
            delete_permission=Permissions.Product_Member_Delete,
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
            request=request,
            object_to_check=obj,
            get_permission=Permissions.Product_Authorization_Group_Member_View,
            put_permission=Permissions.Product_Authorization_Group_Member_Edit,
            delete_permission=Permissions.Product_Authorization_Group_Member_Delete,
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
            request=request,
            object_to_check=obj,
            get_permission=Permissions.Branch_View,
            put_permission=Permissions.Branch_Edit,
            delete_permission=Permissions.Branch_Delete,
        )


class UserHasServicePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request=request,
            object_to_check=obj,
            get_permission=Permissions.Service_View,
            put_permission=None,
            delete_permission=Permissions.Service_Delete,
        )


class UserHasObservationPermission(BasePermission):
    def has_permission(self, request, view):
        if request.path.endswith("/bulk_assessment/"):
            return True

        return check_post_permission(
            request, Product, "product", Permissions.Observation_Create
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permission(
            request=request,
            object_to_check=obj,
            get_permission=Permissions.Observation_View,
            put_permission=Permissions.Observation_Edit,
            delete_permission=Permissions.Observation_Delete,
        )
