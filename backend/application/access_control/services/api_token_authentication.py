from typing import Optional

from argon2 import PasswordHasher
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from application.access_control.models import API_Token, User

API_TOKEN_PREFIX = "APIToken"  # nosec B105


class APITokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple[User, None]]:
        authentication_header = get_authorization_header(request).split()

        if not authentication_header:
            return None

        if len(authentication_header) == 1:
            raise AuthenticationFailed("Invalid token header: No credentials provided.")

        if len(authentication_header) > 2:
            raise AuthenticationFailed("Invalid token header: Token string should not contain spaces.")

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

    def authenticate_header(self, request: Request) -> str:
        return API_TOKEN_PREFIX

    def _validate_api_token(self, api_token: str) -> Optional[User]:
        ph = PasswordHasher()
        api_tokens = API_Token.objects.all()
        for api_token_data in api_tokens:
            try:
                ph.verify(api_token_data.api_token_hash, api_token)
                return api_token_data.user
            except Exception:  # nosec B110
                # all token need to be checked if a valid one can be found
                pass
        return None
