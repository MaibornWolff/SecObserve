from typing import Optional

from django.db.models import Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.licenses.models import License_Group
from application.licenses.queries.license_policy_item import get_license_policy_items


def get_license_group(license_group_id: int) -> Optional[License_Group]:
    try:
        return License_Group.objects.get(id=license_group_id)
    except License_Group.DoesNotExist:
        return None


def get_license_groups() -> QuerySet[License_Group]:
    user = get_current_user()

    if user is None:
        return License_Group.objects.none()

    license_groups = License_Group.objects.all().order_by("id")

    if user.is_superuser:
        return license_groups

    license_policy_items = get_license_policy_items()

    return license_groups.filter(
        Q(users=user)
        | Q(authorization_groups__users=user)
        | Q(is_public=True)
        | Q(license_policy_items__in=license_policy_items)
    ).distinct()
