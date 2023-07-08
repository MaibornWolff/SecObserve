from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.queries.product import get_product_by_id
from application.metrics.api.filters import ProductMetricsFilter
from application.metrics.api.serializers import ProductMetricsSerializer
from application.metrics.models import Product_Metrics
from application.metrics.queries.product_metrics import get_product_metrics
from application.metrics.services.metrics import (
    get_severity_counts,
    get_severity_timeline,
    get_status_counts,
)


class ProductMetricsViewSet(GenericViewSet, ListModelMixin):
    serializer_class = ProductMetricsSerializer
    filterset_class = ProductMetricsFilter
    queryset = Product_Metrics.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return get_product_metrics()


class ProductMetricsCountsView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product_id = request.query_params.get("product_id")
        if product_id:
            product = get_product_by_id(product_id)
        else:
            product = None
        if product:
            user_has_permission_or_403(product, Permissions.Product_View)

        age = request.query_params.get("age", "")

        return Response(get_severity_timeline(product, age))


class SeverityCountsView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product_id = request.query_params.get("product_id")
        if product_id:
            product = get_product_by_id(product_id)
        else:
            product = None
        if product:
            user_has_permission_or_403(product, Permissions.Product_View)

        return Response(get_severity_counts(product))


class StatusCountsView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product_id = request.query_params.get("product_id")
        if product_id:
            product = get_product_by_id(product_id)
        else:
            product = None
        if product:
            user_has_permission_or_403(product, Permissions.Product_View)

        return Response(get_status_counts(product))
