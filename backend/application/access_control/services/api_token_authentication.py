import secrets
import string
from typing import Optional

from argon2 import PasswordHasher
from argon2.profiles import RFC_9106_LOW_MEMORY
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from application.access_control.models import API_Token, User

API_TOKEN_PREFIX = "APIToken"


def create_api_token(user: User) -> str:
    try:
        API_Token.objects.get(user=user)
        raise ValidationError("Only one API token per user is allowed.")
    except API_Token.DoesNotExist:
        pass

    alphabet = string.ascii_letters + string.digits
    api_token = "".join(secrets.choice(alphabet) for i in range(32))

    ph = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)
    api_token_hash = ph.hash(api_token)

    API_Token(user=user, api_token_hash=api_token_hash).save()

    return api_token


def revoke_api_token(user: User) -> None:
    api_tokens = API_Token.objects.filter(user=user)
    for api_token in api_tokens:
        api_token.delete()


class APITokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authentication_header = get_authorization_header(request).split()

        if not authentication_header:
            return None

        if len(authentication_header) == 1:
            raise AuthenticationFailed("Invalid token header: No credentials provided.")

        if len(authentication_header) > 2:
            raise AuthenticationFailed(
                "Invalid token header: Token string should not contain spaces."
            )

        auth_prefix = authentication_header[0].decode("UTF-8")
        auth_token = authentication_header[1].decode("UTF-8")

        if auth_prefix.lower() != API_TOKEN_PREFIX.lower():
            # Authorization header is possibly for another backend
            return None

        user = self._validate_api_token(auth_token)
        if not user:
            raise AuthenticationFailed("Invalid API token.")

        if not user.is_active:
            raise AuthenticationFailed("User is deactivated.")

        return (user, None)

    def authenticate_header(self, request):
        return API_TOKEN_PREFIX

    def _validate_api_token(self, api_token: str) -> Optional[User]:
        ph = PasswordHasher()
        api_tokens = API_Token.objects.all()
        for api_token_data in api_tokens:
            try:
                ph.verify(api_token_data.api_token_hash, api_token)
                return api_token_data.user
            except Exception:
                # all token need to be checked if a valid one can be found
                pass
        return None
