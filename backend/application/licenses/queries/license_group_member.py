from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import User
from application.access_control.queries.user import get_users
from application.commons.services.global_request import get_current_user
from application.licenses.models import License_Group, License_Group_Member
from application.licenses.queries.license_group import get_license_groups


def get_license_group_member(
    license_group: License_Group, user: User
) -> Optional[License_Group_Member]:
    try:
        return License_Group_Member.objects.get(license_group=license_group, user=user)
    except License_Group_Member.DoesNotExist:
        return None


def get_license_group_members() -> QuerySet[License_Group_Member]:
    user = get_current_user()

    if user is None:
        return License_Group_Member.objects.none()

    license_group_members = License_Group_Member.objects.all().order_by("id")

    if user.is_superuser:
        return license_group_members

    license_groups = get_license_groups()
    users = get_users()

    return license_group_members.filter(
        license_group__in=license_groups, user__in=users
    )
