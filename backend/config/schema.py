from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_bearer_security_scheme_object

from application.access_control.services.api_token_authentication import (
    API_TOKEN_PREFIX,
)
from application.access_control.services.jwt_authentication import JWT_PREFIX


class APITokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "application.access_control.services.api_token_authentication.APITokenAuthentication"
    name = "API token authentication"

    def get_security_definition(self, auto_schema: AutoSchema) -> dict | list[dict]:
        return build_bearer_security_scheme_object(
            header_name="AUTHORIZATION",
            token_prefix=API_TOKEN_PREFIX,
        )


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "application.access_control.services.jwt_authentication.JWTAuthentication"
    name = "JWT authentication"

    def get_security_definition(self, auto_schema: AutoSchema) -> dict | list[dict]:
        return build_bearer_security_scheme_object(
            header_name="AUTHORIZATION",
            token_prefix=JWT_PREFIX,
        )


class AdfsAccessTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "django_auth_adfs.rest_framework.AdfsAccessTokenAuthentication"
    name = "OAauth2 authentication"

    def get_security_definition(self, auto_schema: AutoSchema) -> dict | list[dict]:
        return build_bearer_security_scheme_object(  # nosec hardcoded_password_funcarg
            header_name="AUTHORIZATION", token_prefix="Bearer", bearer_format="JWT"
        )
