from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import User
from application.access_control.queries.user import get_users
from application.commons.services.global_request import get_current_user
from application.licenses.models import License_Policy, License_Policy_Member
from application.licenses.queries.license_policy import get_license_policies


def get_license_policy_member(
    license_policy: License_Policy, user: User
) -> Optional[License_Policy_Member]:
    try:
        return License_Policy_Member.objects.get(
            license_policy=license_policy, user=user
        )
    except License_Policy_Member.DoesNotExist:
        return None


def get_license_policy_members() -> QuerySet[License_Policy_Member]:
    user = get_current_user()

    if user is None:
        return License_Policy_Member.objects.none()

    license_policy_members = License_Policy_Member.objects.all().order_by("id")

    if user.is_superuser:
        return license_policy_members

    license_policies = get_license_policies()
    users = get_users()
    return license_policy_members.filter(
        license_policy__in=license_policies, user__in=users
    )
