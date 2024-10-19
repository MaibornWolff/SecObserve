from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from application.licenses.models import (
    License_Group,
    License_Group_Member,
    License_Policy,
    License_Policy_Member,
)


class UserHasLicenseGroupPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj: License_Group):
        if request.method != "GET":
            return _has_license_policy_manage_permission(request, obj)

        return True


class UserHasLicenseGroupMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            license_group = get_object_or_404(
                License_Group_Member, pk=request.data.get("license_group")
            )
            return _has_license_group_manage_permission(request, license_group)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method != "GET":
            return _has_license_group_manage_permission(request, obj.license_policy)

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

    def has_object_permission(self, request, view, obj):
        if request.method != "GET":
            return _has_license_policy_manage_permission(request, obj.license_policy)

        return True


def _has_license_group_manage_permission(request, license_group: License_Group) -> bool:
    user = request.user
    if user and user.is_superuser:
        return True

    try:
        license_group_member = License_Group_Member.objects.get(
            license_policy=license_group, user=user
        )
        return license_group_member.is_manager
    except License_Group_Member.DoesNotExist:
        return False


def _has_license_policy_manage_permission(
    request, license_policy: License_Policy
) -> bool:
    user = request.user
    if user and user.is_superuser:
        return True

    try:
        license_policy_member = License_Policy_Member.objects.get(
            license_policy=license_policy, user=user
        )
        return license_policy_member.is_manager
    except License_Policy_Member.DoesNotExist:
        return False
