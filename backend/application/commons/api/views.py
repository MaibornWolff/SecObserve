from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from application.commons.api.filters import NotificationFilter
from application.commons.api.permissions import UserHasNotificationPermission
from application.commons.api.serializers import (
    NotificationBulkSerializer,
    NotificationSerializer,
    VersionSerializer,
)
from application.commons.models import Notification
from application.commons.queries.notification import get_notifications
from application.commons.services.notification import bulk_delete


class VersionView(APIView):
    serializer_class = VersionSerializer

    @action(detail=True, methods=["get"], url_name="version")
    def get(self, request):
        content = {
            "version": "version_unkown",
        }
        return Response(content)


class HealthView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None

    @action(detail=True, methods=["get"], url_name="health")
    def get(self, request):
        response = Response()
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"

        return response


class NotificationViewSet(
    GenericViewSet, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
):
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilter
    permission_classes = (IsAuthenticated, UserHasNotificationPermission)
    queryset = Notification.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self):
        return get_notifications()

    @extend_schema(
        methods=["POST"],
        request=NotificationBulkSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=False, methods=["post"])
    def bulk_delete(self, request):
        request_serializer = NotificationBulkSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        bulk_delete(request_serializer.validated_data.get("notifications"))

        return Response(status=HTTP_204_NO_CONTENT)
