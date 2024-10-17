from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from application.licenses.models import License_Policy, License_Policy_Member


class UserHasLicensePolicyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_external

        return True

    def has_object_permission(self, request, view, obj: License_Policy):
        if request.method != "GET":
            return _has_manage_permission(request, obj)

        return True


class UserHasLicensePolicyItemMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            license_policy = get_object_or_404(
                License_Policy, pk=request.data.get("license_policy")
            )
            return _has_manage_permission(request, license_policy)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method != "GET":
            return _has_manage_permission(request, obj.license_policy)

        return True


def _has_manage_permission(request, license_policy: License_Policy) -> bool:
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
