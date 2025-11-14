from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import API_Token, User
from application.access_control.services.current_user import get_current_user


def get_api_token_by_id(pk: int) -> Optional[API_Token]:
    try:
        return API_Token.objects.get(pk=pk)
    except API_Token.DoesNotExist:
        return None


def get_api_tokens() -> QuerySet[API_Token]:
    user = get_current_user()

    if user is None:
        return API_Token.objects.none()

    api_tokens = API_Token.objects.all()

    if user.is_superuser:
        return api_tokens

    return api_tokens.filter(user=user)


def get_api_tokens_for_user(given_user: User) -> QuerySet[API_Token]:
    current_user = get_current_user()

    if current_user is None:
        return API_Token.objects.none()

    api_tokens = API_Token.objects.filter(user=given_user)

    if current_user.is_superuser:
        return api_tokens

    return api_tokens if current_user == given_user else API_Token.objects.none()
