from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import Authorization_Group
from application.commons.services.global_request import get_current_user
from application.core.queries.product_member import (
    get_product_authorization_group_members,
)


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

    if user.is_superuser or not user.is_external:
        return authorization_groups

    product_authorization_group_members = get_product_authorization_group_members()

    return authorization_groups.filter(
        id__in=[
            member.authorization_group_id
            for member in product_authorization_group_members
        ]
    )
