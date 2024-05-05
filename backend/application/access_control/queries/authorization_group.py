from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import Authorization_Group
from application.commons.services.global_request import get_current_user


def get_authorization_group_by_id(pk: int) -> Optional[Authorization_Group]:
    try:
        return Authorization_Group.objects.get(pk=pk)
    except Authorization_Group.DoesNotExist:
        return None


def get_authorization_groups() -> QuerySet[Authorization_Group]:
    user = get_current_user()

    if user is None:
        return Authorization_Group.objects.none()

    authorization_groups = Authorization_Group.objects.all()

    if user.is_superuser:
        return authorization_groups

    return authorization_groups.filter(users=user)
