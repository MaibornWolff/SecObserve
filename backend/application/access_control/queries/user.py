from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import User
from application.commons.services.global_request import get_current_user
from application.core.queries.product_member import get_product_members


def get_user_by_id(pk: int) -> Optional[User]:
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        return None


def get_user_by_username(username: str) -> Optional[User]:
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def get_user_by_email(email: str) -> Optional[User]:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None


def get_users() -> QuerySet[User]:
    user = get_current_user()

    if user is None:
        return User.objects.none()

    users = User.objects.all()

    if user.is_superuser or not user.is_external:
        return users

    product_members = get_product_members()

    return users.filter(id__in=[member.user_id for member in product_members])


def get_users_without_api_tokens() -> QuerySet[User]:
    user = get_current_user()

    if user is None:
        return User.objects.none()

    users = User.objects.exclude(username__startswith="-product-")

    if user.is_superuser or not user.is_external:
        return users

    product_members = get_product_members()

    return users.filter(id__in=[member.user_id for member in product_members])
