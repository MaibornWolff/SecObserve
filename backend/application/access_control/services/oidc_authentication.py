import os
from typing import Optional

import jwt
import requests
from django.db import IntegrityError, transaction
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from application.access_control.models import User
from application.access_control.queries.user import get_user_by_username

OIDC_PREFIX = "Bearer"
ALGORITHMS = ["RS256", "RS384", "RS512", "ES256 ", "ES384", "ES512", "EdDSA"]


class OIDCAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            return None

        if len(auth) == 1:
            raise AuthenticationFailed("Invalid token header: No credentials provided.")

        if len(auth) > 2:
            raise AuthenticationFailed(
                "Invalid token header: Token string should not contain spaces."
            )

        auth_prefix = auth[0].decode("UTF-8")
        auth_token = auth[1].decode("UTF-8")

        if auth_prefix.lower() != OIDC_PREFIX.lower():
            # Authorization header is possibly for another backend
            return None

        user = self._validate_jwt(auth_token)
        if not user:
            raise AuthenticationFailed("Invalid token.")

        if not user.is_active:
            raise AuthenticationFailed("User is deactivated.")

        return (user, None)

    def authenticate_header(self, request):
        return OIDC_PREFIX

    def _validate_jwt(self, token: str) -> Optional[User]:
        try:
            jwks_uri = self._get_jwks_uri()
            jwks_client = jwt.PyJWKClient(jwks_uri)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            options = {
                "verify_signature": True,
                "verify_aud": True,
                "strict_aud": True,
                "require": ["exp"],
                "verify_iat": True,
                "verify_exp": True,
                "verify_nbf": True,
            }
            payload = jwt.decode(
                jwt=token,
                options=options,
                key=signing_key.key,
                algorithms=ALGORITHMS,
                audience=os.environ["OIDC_CLIENT_ID"],
            )
            username = payload.get(os.environ["OIDC_USERNAME"])
            user = get_user_by_username(username)
            if user:
                user = self._check_user_change(user, payload)
                return user
            return self._create_user(username, payload)
        except jwt.PyJWTError as e:
            raise AuthenticationFailed(str(e)) from e

    def _get_jwks_uri(self):
        response = requests.request(
            method="GET",
            url=f"{os.environ['OIDC_AUTHORITY']}/.well-known/openid-configuration",
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["jwks_uri"]

    def _create_user(self, username: str, payload: dict) -> User:
        user = User(username=username, first_name="", last_name="", email="")
        if os.environ.get("OIDC_EMAIL"):
            user.email = payload[os.environ["OIDC_EMAIL"]]
        if os.environ.get("OIDC_FIRST_NAME"):
            user.first_name = payload[os.environ["OIDC_FIRST_NAME"]]
        if os.environ.get("OIDC_LAST_NAME"):
            user.last_name = payload[os.environ["OIDC_LAST_NAME"]]
        try:
            with transaction.atomic():
                user.save()
            return user
        except IntegrityError as e:
            # User was most likely created by another request
            existing_user = get_user_by_username(username)
            if not existing_user:
                raise e
            return existing_user

    def _check_user_change(self, user: User, payload: dict) -> User:
        user_changed = False
        if (
            os.environ.get("OIDC_EMAIL")
            and user.email != payload[os.environ["OIDC_EMAIL"]]
        ):
            user.email = payload[os.environ["OIDC_EMAIL"]]
            user_changed = True
        if (
            os.environ.get("OIDC_FIRST_NAME")
            and user.first_name != payload[os.environ["OIDC_FIRST_NAME"]]
        ):
            user.first_name = payload[os.environ["OIDC_FIRST_NAME"]]
            user_changed = True
        if (
            os.environ.get("OIDC_LAST_NAME")
            and user.last_name != payload[os.environ["OIDC_LAST_NAME"]]
        ):
            user.last_name = payload[os.environ["OIDC_LAST_NAME"]]
            user_changed = True
        if user_changed:
            user.save()
        return user
