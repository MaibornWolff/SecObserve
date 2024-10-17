from typing import Optional

from django.db.models.query import Q, QuerySet

from application.commons.services.global_request import get_current_user
from application.licenses.models import License_Policy


def get_license_policy(license_policy_id: int) -> Optional[License_Policy]:
    try:
        return License_Policy.objects.get(id=license_policy_id)
    except License_Policy.DoesNotExist:
        return None


def get_license_policys() -> QuerySet[License_Policy]:
    user = get_current_user()

    if user is None:
        return License_Policy.objects.none()

    license_policys = License_Policy.objects.all()

    if user.is_superuser:
        return license_policys

    return license_policys.filter(Q(users=user) | Q(is_public=True))
