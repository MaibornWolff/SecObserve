from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.licenses.api.filters import LicenseFilter, LicenseGroupFilter
from application.licenses.api.serializers import (
    LicenseGroupSerializer,
    LicenseSerializer,
)
from application.licenses.models import License, License_Group


class LicenseViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = LicenseSerializer
    filterset_class = LicenseFilter
    queryset = License.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]


class LicenseGroupViewSet(ModelViewSet):
    serializer_class = LicenseGroupSerializer
    filterset_class = LicenseGroupFilter
    queryset = License_Group.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
