from typing import Union

from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from application.commons.api.filters import NotificationFilter
from application.commons.api.permissions import (
    UserHasNotificationPermission,
    UserHasSuperuserPermission,
)
from application.commons.api.serializers import (
    NotificationBulkSerializer,
    NotificationSerializer,
    SettingsSerializer,
    StatusSettingsSerializer,
    VersionSerializer,
)
from application.commons.models import Notification, Notification_Viewed, Settings
from application.commons.queries.notification import (
    get_notification_by_id,
    get_notifications,
)
from application.commons.services.notification import bulk_mark_as_viewed


class VersionView(APIView):
    serializer_class = VersionSerializer

    @action(detail=True, methods=["get"], url_name="version")
    def get(self, request: Request) -> Response:
        content = {
            "version": "version_unknown",
        }
        return Response(content)


class HealthView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None

    @action(detail=True, methods=["get"], url_name="health")
    def get(self, request: Request) -> Response:
        response = Response()
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"

        return response


class StatusSettingsView(APIView):
    serializer_class = StatusSettingsSerializer
    permission_classes = []

    @action(detail=True, methods=["get"], url_name="settings")
    def get(self, request: Request) -> Response:
        features = []

        settings = Settings.load()
        if settings.feature_disable_user_login:
            features.append("feature_disable_user_login")

        if request.user.is_authenticated:
            if settings.feature_vex:
                features.append("feature_vex")
            if settings.feature_general_rules_need_approval:
                features.append("feature_general_rules_need_approval")
            if settings.feature_license_management:
                features.append("feature_license_management")
            if settings.feature_automatic_api_import:
                features.append("feature_automatic_api_import")
            if settings.feature_automatic_osv_scanning:
                features.append("feature_automatic_osv_scanning")
            if settings.feature_exploit_information:
                features.append("feature_exploit_information")

        content: dict[str, Union[int, list[str]]] = {
            "features": features,
        }

        if request.user.is_authenticated:
            content["risk_acceptance_expiry_days"] = settings.risk_acceptance_expiry_days

        return Response(content)


class SettingsView(APIView):
    serializer_class = SettingsSerializer
    permission_classes = (IsAuthenticated, UserHasSuperuserPermission)

    @action(detail=True, methods=["get"], url_name="settings")
    def get(self, request: Request, pk: int = None) -> Response:  # pylint: disable=unused-argument
        # pk is needed for the API signature but we don't need it
        settings = Settings.load()
        response_serializer = SettingsSerializer(settings)
        return Response(response_serializer.data)

    @action(detail=True, methods=["patch"], url_name="settings")
    def patch(self, request: Request, pk: int = None) -> Response:  # pylint: disable=unused-argument
        # pk is needed for the API signature but we don't need it
        request_serializer = SettingsSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        settings = Settings.load()
        request_serializer.update(settings, request_serializer.validated_data)

        response_serializer = SettingsSerializer(settings)
        return Response(response_serializer.data)


class NotificationViewSet(GenericViewSet, DestroyModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilter
    permission_classes = (IsAuthenticated, UserHasNotificationPermission)
    queryset = Notification.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self) -> QuerySet[Notification]:
        return get_notifications()

    @extend_schema(
        methods=["POST"],
        request=NotificationBulkSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=False, methods=["post"])
    def bulk_mark_as_viewed(self, request: Request) -> Response:
        request_serializer = NotificationBulkSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        bulk_mark_as_viewed(request_serializer.validated_data.get("notifications"))

        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["POST"],
        request=None,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def mark_as_viewed(self, request: Request, pk: int = None) -> Response:
        if not get_notification_by_id(pk):
            return Response(status=HTTP_404_NOT_FOUND)

        Notification_Viewed.objects.update_or_create(
            notification_id=pk,
            user=request.user,
        )
        return Response(status=HTTP_204_NO_CONTENT)
