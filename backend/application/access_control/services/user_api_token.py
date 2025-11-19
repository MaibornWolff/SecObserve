import secrets
import string
from datetime import date

from argon2 import PasswordHasher
from argon2.profiles import RFC_9106_LOW_MEMORY
from rest_framework.exceptions import ValidationError

from application.access_control.models import API_Token_Multiple, User


def create_user_api_token(user: User, name: str, expiration_date: date) -> str:
    try:
        API_Token_Multiple.objects.get(user=user, name=name)
        raise ValidationError("API token with this name already exists.")
    except API_Token_Multiple.DoesNotExist:
        pass

    api_token, api_token_hash = generate_api_token_hash()

    API_Token_Multiple(user=user, name=name, api_token_hash=api_token_hash, expiration_date=expiration_date).save()

    return api_token


def revoke_user_api_token(user: User, name: str) -> None:
    try:
        api_token = API_Token_Multiple.objects.get(user=user, name=name)
        api_token.delete()
    except API_Token_Multiple.DoesNotExist:
        pass


def generate_api_token_hash() -> tuple[str, str]:
    alphabet = string.ascii_letters + string.digits
    api_token = "".join(secrets.choice(alphabet) for i in range(32))
    api_token = f"api_token_{api_token}"

    ph = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)
    api_token_hash = ph.hash(api_token)

    return api_token, api_token_hash
