from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import User
from application.commons.services.global_request import get_current_user
from application.core.queries.product import get_product_members


def get_user_by_username(username: str) -> Optional[User]:
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def get_users() -> QuerySet[User]:
    user = get_current_user()

    if user is None:
        return User.objects.none()

    if user.is_superuser or not user.is_external:
        return User.objects.all()

    product_members = get_product_members()

    return User.objects.filter(id__in=[member.user_id for member in product_members])
