from typing import Optional

from django.db.models.query import Q, QuerySet

from application.commons.services.global_request import get_current_user
from application.licenses.models import License_Group


def get_license_group(license_group_id: int) -> Optional[License_Group]:
    try:
        return License_Group.objects.get(id=license_group_id)
    except License_Group.DoesNotExist:
        return None


def get_license_groups() -> QuerySet[License_Group]:
    user = get_current_user()

    if user is None:
        return License_Group.objects.none()

    license_groups = License_Group.objects.all()

    if user.is_superuser:
        return license_groups

    return license_groups.filter(Q(users=user) | Q(is_public=True))
