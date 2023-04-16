import logging

from django.contrib.auth import authenticate as django_authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from application.access_control.api.filters import UserFilter
from application.access_control.api.serializers import (
    AuthenticationRequestSerializer,
    AuthenticationResponseSerializer,
    CreateAPITokenResponseSerializer,
    UserSerializer,
    UserSettingsSerializer,
)
from application.access_control.models import User
from application.access_control.queries.user import get_users
from application.access_control.services.api_token_authentication import (
    create_api_token,
    revoke_api_token,
)
from application.access_control.services.jwt_authentication import create_jwt
from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.access_control")


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    filterset_class = UserFilter
    queryset = User.objects.none()

    def get_queryset(self):
        return get_users()

    @extend_schema(methods=["GET"], responses={status.HTTP_200_OK: UserSerializer})
    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        methods=["PATCH"],
        request=UserSettingsSerializer,
        responses={status.HTTP_200_OK: UserSerializer},
    )
    @action(detail=False, methods=["patch"])
    def my_settings(self, request):
        request_serializer = UserSettingsSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        setting_theme = request_serializer.validated_data.get("setting_theme")
        user = request.user
        if setting_theme:
            user.setting_theme = setting_theme
        user.save()

        response_serializer = UserSerializer(request.user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class CreateAPITokenView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=AuthenticationRequestSerializer,
        responses={status.HTTP_200_OK: CreateAPITokenResponseSerializer},
    )
    def post(self, request):
        user = get_authenticated_user(request.data)
        try:
            token = create_api_token(user)
        except ValidationError as e:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            logger.warning(
                format_log_message(message=str(e), user=user, response=response)
            )
            raise

        response = Response({"token": token})
        logger.info(
            format_log_message(
                message="API token created", user=user, response=response
            )
        )
        return response


class RevokeAPITokenView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=AuthenticationRequestSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request):
        user = get_authenticated_user(request.data)
        revoke_api_token(user)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        logger.info(
            format_log_message(
                message="API token revoked", user=user, response=response
            )
        )
        return response


class AuthenticateView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=AuthenticationRequestSerializer,
        responses={status.HTTP_200_OK: AuthenticationResponseSerializer},
    )
    def post(self, request):
        user = get_authenticated_user(request.data)

        jwt = create_jwt(user)

        user_serializer = UserSerializer(user)
        response = Response({"jwt": jwt, "user": user_serializer.data})
        logger.info(
            format_log_message(
                message="User authenticated", user=user, response=response
            )
        )
        return response


def get_authenticated_user(data) -> User:
    request_serializer = AuthenticationRequestSerializer(data=data)
    if not request_serializer.is_valid():
        raise ValidationError(request_serializer.errors)

    username = request_serializer.validated_data.get("username")
    password = request_serializer.validated_data.get("password")

    user: User = django_authenticate(username=username, password=password)  # type: ignore[assignment]
    # We always get a User from our model
    if not user:
        raise PermissionDenied("Invalid credentials")

    return user
