from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from application.background_tasks.api.filters import PeriodicTaskFilter
from application.background_tasks.api.serializers import PeriodicTaskSerializer
from application.background_tasks.models import Periodic_Task
from application.commons.api.permissions import UserHasSuperuserPermission


class PeriodicTaskViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = PeriodicTaskSerializer
    filterset_class = PeriodicTaskFilter
    permission_classes = [IsAuthenticated, UserHasSuperuserPermission]
    queryset = Periodic_Task.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["task"]
