import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional

from constance import config
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)

from application.access_control.models import User
from application.access_control.queries.user import get_user_by_username
from application.access_control.services.jwt_secret import get_secret

ALGORITHM = "HS256"
JWT_PREFIX = "JWT"


def create_jwt(user: User) -> str:
    if user.is_superuser:
        jwt_validity_duration = config.JWT_VALIDITY_DURATION_SUPERUSER
    else:
        jwt_validity_duration = config.JWT_VALIDITY_DURATION_USER

    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=jwt_validity_duration),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
    }
    token = jwt.encode(payload, get_secret(), algorithm=ALGORITHM)
    return token


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None
        elif len(auth) == 1:
            raise AuthenticationFailed("Invalid token header: No credentials provided.")
        elif len(auth) > 2:
            raise AuthenticationFailed(
                "Invalid token header: Token string should not contain spaces."
            )

        auth_prefix = auth[0].decode("UTF-8")
        auth_token = auth[1].decode("UTF-8")

        if auth_prefix.lower() != JWT_PREFIX.lower():
            # Authorization header is possibly for another backend
            return None

        user = self._validate_jwt(auth_token)
        if user:
            if user.is_active:
                return (user, None)
            else:
                raise AuthenticationFailed("User is deactivated.")
        else:
            raise AuthenticationFailed("Invalid token.")

    def authenticate_header(self, request):
        return JWT_PREFIX

    def _validate_jwt(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, get_secret(), algorithms=[ALGORITHM])
            username = payload.get("username")
            if not username:
                raise AuthenticationFailed("No username in JWT")
            return get_user_by_username(username)
        except jwt.PyJWTError as e:
            raise AuthenticationFailed(str(e))
