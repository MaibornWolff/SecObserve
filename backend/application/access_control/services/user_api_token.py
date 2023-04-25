import secrets
import string

from argon2 import PasswordHasher
from argon2.profiles import RFC_9106_LOW_MEMORY
from rest_framework.exceptions import ValidationError

from application.access_control.models import API_Token, User


def create_user_api_token(user: User) -> str:
    try:
        API_Token.objects.get(user=user)
        raise ValidationError("Only one API token per user is allowed.")
    except API_Token.DoesNotExist:
        pass

    api_token, api_token_hash = generate_api_token_hash()

    API_Token(user=user, api_token_hash=api_token_hash).save()

    return api_token


def revoke_user_api_token(user: User) -> None:
    api_tokens = API_Token.objects.filter(user=user)
    for api_token in api_tokens:
        api_token.delete()


def generate_api_token_hash() -> tuple[str, str]:
    alphabet = string.ascii_letters + string.digits
    api_token = "".join(secrets.choice(alphabet) for i in range(32))
    api_token = f"api_token_{api_token}"

    ph = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)
    api_token_hash = ph.hash(api_token)

    return api_token, api_token_hash
