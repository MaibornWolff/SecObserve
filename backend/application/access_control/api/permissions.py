from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from application.access_control.models import (
    Authorization_Group,
    Authorization_Group_Member,
)


class UserHasSuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method != "GET"
            and request.path != "/api/users/my_settings/"
            and not request.path.endswith("/change_password/")
        ):
            return request.user.is_superuser

        return True

    def has_object_permission(self, request, view, obj):
        if (
            request.method != "GET"
            and request.path != f"/api/users/{obj.pk}/change_password/"
        ):
            return request.user.is_superuser

        return True


class UserHasAuthorizationGroupPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj: Authorization_Group):
        if request.method != "GET":
            return _has_manage_permission(request, obj)

        return True


class UserHasAuthorizationGroupMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            authorization_group = get_object_or_404(
                Authorization_Group, pk=request.data.get("authorization_group")
            )
            return _has_manage_permission(request, authorization_group)

        return True

    def has_object_permission(self, request, view, obj: Authorization_Group_Member):
        if request.method != "GET":
            return _has_manage_permission(request, obj.authorization_group)

        return True


def _has_manage_permission(request, authorization_group: Authorization_Group) -> bool:
    user = request.user
    if user and user.is_superuser:
        return True

    try:
        authorization_group_member = Authorization_Group_Member.objects.get(
            authorization_group=authorization_group, user=user
        )
        return authorization_group_member.is_manager
    except Authorization_Group_Member.DoesNotExist:
        return False
