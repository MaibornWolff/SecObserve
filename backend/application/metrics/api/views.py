from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.models import Observation
from application.core.queries.product import get_product_by_id
from application.metrics.services.metrics import get_severity_counts, get_status_counts


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

        data = get_severity_counts(product=product)
        response_data = {}
        response_data[Observation.SEVERITY_CRITICAL] = self.get_severity_count(
            Observation.SEVERITY_CRITICAL, data
        )
        response_data[Observation.SEVERITY_HIGH] = self.get_severity_count(
            Observation.SEVERITY_HIGH, data
        )
        response_data[Observation.SEVERITY_MEDIUM] = self.get_severity_count(
            Observation.SEVERITY_MEDIUM, data
        )
        response_data[Observation.SEVERITY_LOW] = self.get_severity_count(
            Observation.SEVERITY_LOW, data
        )
        response_data[Observation.SEVERITY_NONE] = self.get_severity_count(
            Observation.SEVERITY_NONE, data
        )
        response_data[Observation.SEVERITY_UNKOWN] = self.get_severity_count(
            Observation.SEVERITY_UNKOWN, data
        )
        return Response(response_data)

    def get_severity_count(self, severity, data):
        for row in data:
            if row.get("current_severity") == severity:
                return row.get("id__count")
        return 0


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

        data = get_status_counts(product=product)
        response_data = {}
        response_data[Observation.STATUS_OPEN] = self.get_status_count(
            Observation.STATUS_OPEN, data
        )
        response_data[Observation.STATUS_RESOLVED] = self.get_status_count(
            Observation.STATUS_RESOLVED, data
        )
        response_data[Observation.STATUS_DUPLICATE] = self.get_status_count(
            Observation.STATUS_DUPLICATE, data
        )
        response_data[Observation.STATUS_FALSE_POSITIVE] = self.get_status_count(
            Observation.STATUS_FALSE_POSITIVE, data
        )
        response_data[Observation.STATUS_IN_REVIEW] = self.get_status_count(
            Observation.STATUS_IN_REVIEW, data
        )
        response_data[Observation.STATUS_NOT_AFFECTED] = self.get_status_count(
            Observation.STATUS_NOT_AFFECTED, data
        )
        response_data[Observation.STATUS_NOT_SECURITY] = self.get_status_count(
            Observation.STATUS_NOT_SECURITY, data
        )
        response_data[Observation.STATUS_RISK_ACCEPTED] = self.get_status_count(
            Observation.STATUS_RISK_ACCEPTED, data
        )
        return Response(response_data)

    def get_status_count(self, severity, data):
        for row in data:
            if row.get("current_status") == severity:
                return row.get("id__count")
        return 0
