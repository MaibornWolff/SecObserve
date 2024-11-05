from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission

from application.access_control.queries.authorization_group import (
    get_authorization_groups,
)
from application.licenses.models import (
    License_Group,
    License_Group_Authorization_Group_Member,
    License_Group_Member,
    License_Policy,
    License_Policy_Authorization_Group_Member,
    License_Policy_Member,
)


class UserHasLicenseGroupPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj: License_Group):
        if request.method != "GET":
            return _has_license_group_manage_permission(request, obj)

        return True


class UserHasLicenseGroupMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            license_group = get_object_or_404(
                License_Group, pk=request.data.get("license_group")
            )
            return _has_license_group_manage_permission(request, license_group)

        return True

    def has_object_permission(self, request, view, obj: License_Group_Member):
        if request.method != "GET":
            return _has_license_group_manage_permission(request, obj.license_group)

        return True


class UserHasLicenseGroupAuthenticationGroupMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            license_group = get_object_or_404(
                License_Group, pk=request.data.get("license_group")
            )

            authorization_groups = get_authorization_groups().values_list(
                "id", flat=True
            )
            if request.data.get("authorization_group") not in authorization_groups:
                raise NotFound("Authorization_Group not found.")

            return _has_license_group_manage_permission(request, license_group)

        return True

    def has_object_permission(self, request, view, obj: License_Group_Member):
        if request.method != "GET":
            return _has_license_group_manage_permission(request, obj.license_group)

        return True


class UserHasLicensePolicyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj: License_Policy):
        if request.method != "GET":
            return _has_license_policy_manage_permission(request, obj)

        return True


class UserHasLicensePolicyItemMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            license_policy = get_object_or_404(
                License_Policy, pk=request.data.get("license_policy")
            )
            return _has_license_policy_manage_permission(request, license_policy)

        return True

    def has_object_permission(self, request, view, obj: License_Policy_Member):
        if request.method != "GET":
            return _has_license_policy_manage_permission(request, obj.license_policy)

        return True


class UserHasLicensePolicyAuthorizationGroupMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            license_policy = get_object_or_404(
                License_Policy, pk=request.data.get("license_policy")
            )

            authorization_groups = get_authorization_groups().values_list(
                "id", flat=True
            )
            if request.data.get("authorization_group") not in authorization_groups:
                raise NotFound("Authorization_Group not found.")

            return _has_license_policy_manage_permission(request, license_policy)

        return True

    def has_object_permission(self, request, view, obj: License_Policy_Member):
        if request.method != "GET":
            return _has_license_policy_manage_permission(request, obj.license_policy)

        return True


def _has_license_group_manage_permission(request, license_group: License_Group) -> bool:
    user = request.user
    if user and user.is_superuser:
        return True

    if License_Group_Member.objects.filter(
        license_group=license_group, user=user, is_manager=True
    ).exists():
        return True

    if License_Group_Authorization_Group_Member.objects.filter(
        license_group=license_group, authorization_group__users=user, is_manager=True
    ).exists():
        return True

    return False


def _has_license_policy_manage_permission(
    request, license_policy: License_Policy
) -> bool:
    user = request.user
    if user and user.is_superuser:
        return True

    if License_Policy_Member.objects.filter(
        license_policy=license_policy, user=user, is_manager=True
    ).exists():
        return True

    if License_Policy_Authorization_Group_Member.objects.filter(
        license_policy=license_policy, authorization_group__users=user, is_manager=True
    ).exists():
        return True

    return False
