import csv
from tempfile import NamedTemporaryFile

from constance import config
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.queries.product import get_product_by_id
from application.core.types import Severity
from application.metrics.models import Product_Metrics_Status
from application.metrics.services.export_metrics import (
    export_product_metrics_csv,
    export_product_metrics_excel,
)
from application.metrics.services.metrics import (
    get_codecharta_metrics,
    get_product_metrics_current,
    get_product_metrics_timeline,
)


class ProductMetricsTimelineView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product = _get_and_check_product(request)
        age = request.query_params.get("age", "")
        return Response(get_product_metrics_timeline(product, age))


class ProductMetricsCurrentView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product = _get_and_check_product(request)
        return Response(get_product_metrics_current(product))


class ProductMetricsExportExcelView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product = _get_and_check_product(request)

        workbook = export_product_metrics_excel(product)

        with NamedTemporaryFile() as tmp:
            workbook.save(
                tmp.name  # nosemgrep: python.lang.correctness.tempfile.flush.tempfile-without-flush
            )
            # export works fine without .flush()
            tmp.seek(0)
            stream = tmp.read()

        response = HttpResponse(
            content=stream,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=product_metrics.xlsx"

        return response


class ProductMetricsExportCsvView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product = _get_and_check_product(request)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=product_metrics.csv"

        export_product_metrics_csv(response, product)

        return response


class ProductMetricsExportCodeChartaView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        product = _get_and_check_product(request)
        if not product:
            raise ValidationError("Product not found")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="secobserve_codecharta_metrics.csv"'
        )

        writer = csv.DictWriter(
            response,
            fieldnames=[
                "source_file",
                "Vulnerabilities_Total".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_CRITICAL}".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_HIGH}".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_MEDIUM}".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_LOW}".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_NONE}".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_UNKOWN}".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_HIGH}_and_above".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_MEDIUM}_and_above".lower(),
                f"Vulnerabilities_{Severity.SEVERITY_LOW}_and_above".lower(),
            ],
        )
        writer.writeheader()
        for row in get_codecharta_metrics(product):
            writer.writerow(row)

        return response


class ProductMetricsStatusView(APIView):
    @action(detail=False, methods=["get"])
    def get(self, request):
        status = Product_Metrics_Status.load()
        return Response(
            {
                "last_calculated": status.last_calculated,
                "calculation_interval": config.BACKGROUND_PRODUCT_METRICS_INTERVAL_MINUTES,
            }
        )


def _get_and_check_product(request):
    product_id = request.query_params.get("product_id")
    if product_id:
        product = get_product_by_id(product_id)
    else:
        product = None
    if product:
        user_has_permission_or_403(product, Permissions.Product_View)
    return product
