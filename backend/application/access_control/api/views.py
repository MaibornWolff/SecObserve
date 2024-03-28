import logging

from django.contrib.auth import authenticate as django_authenticate
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet

from application.access_control.api.filters import AuthorizationGroupFilter, UserFilter
from application.access_control.api.serializers import (
    AuthenticationRequestSerializer,
    AuthenticationResponseSerializer,
    AuthorizationGroupSerializer,
    CreateApiTokenResponseSerializer,
    ProductApiTokenSerializer,
    UserSerializer,
    UserSettingsSerializer,
)
from application.access_control.models import Authorization_Group, User
from application.access_control.queries.authorization_group import (
    get_authorization_groups,
)
from application.access_control.queries.user import (
    get_users,
    get_users_without_api_tokens,
)
from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.jwt_authentication import create_jwt
from application.access_control.services.product_api_token import (
    create_product_api_token,
    get_product_api_tokens,
    revoke_product_api_token,
)
from application.access_control.services.roles_permissions import Permissions
from application.access_control.services.user_api_token import (
    create_user_api_token,
    revoke_user_api_token,
)
from application.commons.services.log_message import format_log_message
from application.core.models import Product
from application.core.queries.product import get_product_by_id

logger = logging.getLogger("secobserve.access_control")


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    filterset_class = UserFilter
    queryset = User.objects.none()

    def get_queryset(self):
        if self.action == "list":
            return get_users_without_api_tokens()

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
        setting_list_size = request_serializer.validated_data.get("setting_list_size")
        setting_list_properties = request_serializer.validated_data.get(
            "setting_list_properties"
        )
        user: User = request.user
        if setting_theme:
            user.setting_theme = setting_theme
        if setting_list_size:
            user.setting_list_size = setting_list_size
        if setting_list_properties:
            user.setting_list_properties = setting_list_properties
        user.save()

        response_serializer = UserSerializer(request.user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class AuthorizationGroupViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = AuthorizationGroupSerializer
    filterset_class = AuthorizationGroupFilter
    queryset = Authorization_Group.objects.none()

    def get_queryset(self):
        return get_authorization_groups()


class CreateUserAPITokenView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=AuthenticationRequestSerializer,
        responses={status.HTTP_201_CREATED: CreateApiTokenResponseSerializer},
    )
    def post(self, request):
        user = _get_authenticated_user(request.data)
        try:
            token = create_user_api_token(user)
        except ValidationError as e:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            logger.warning(
                format_log_message(message=str(e), user=user, response=response)
            )
            raise

        response = Response({"token": token}, status=status.HTTP_201_CREATED)
        logger.info(
            format_log_message(
                message="API token created", user=user, response=response
            )
        )
        return response


class RevokeUserAPITokenView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=AuthenticationRequestSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request):
        user = _get_authenticated_user(request.data)
        revoke_user_api_token(user)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        logger.info(
            format_log_message(
                message="API token revoked", user=user, response=response
            )
        )
        return response


class ProductApiTokenViewset(ViewSet):
    serializer_class = ProductApiTokenSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="product", location=OpenApiParameter.QUERY, required=True, type=int
            ),
        ],
    )
    def list(self, request):
        product = _get_product(request.query_params.get("product"))
        user_has_permission_or_403(product, Permissions.Product_View)
        tokens = get_product_api_tokens(product)
        serializer = ProductApiTokenSerializer(tokens, many=True)
        response_data = {"results": serializer.data}
        return Response(response_data)

    @extend_schema(
        request=ProductApiTokenSerializer,
        responses={status.HTTP_200_OK: CreateApiTokenResponseSerializer},
    )
    def create(self, request):
        request_serializer = ProductApiTokenSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        product = _get_product(request_serializer.validated_data.get("id"))

        user_has_permission_or_403(product, Permissions.Product_Api_Token_Create)

        token = create_product_api_token(
            product, request_serializer.validated_data.get("role")
        )

        response = Response({"token": token}, status=status.HTTP_201_CREATED)
        logger.info(
            format_log_message(message="Product API token created", response=response)
        )
        return response

    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def destroy(self, request, pk=None):
        product = _get_product(pk)
        user_has_permission_or_403(product, Permissions.Product_Api_Token_Revoke)

        revoke_product_api_token(product)

        response = Response(status=status.HTTP_204_NO_CONTENT)
        logger.info(
            format_log_message(message="Product API token revoked", response=response)
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
        user = _get_authenticated_user(request.data)

        jwt = create_jwt(user)

        user_serializer = UserSerializer(user)
        response = Response({"jwt": jwt, "user": user_serializer.data})
        logger.info(
            format_log_message(
                message="User authenticated", user=user, response=response
            )
        )
        return response


def _get_authenticated_user(data: dict) -> User:
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


def _get_product(product_id: int) -> Product:
    product = get_product_by_id(product_id)
    if not product:
        raise ValidationError(f"Product {product_id} does not exist")

    return product
