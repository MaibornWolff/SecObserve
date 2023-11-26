from typing import Optional

from django.db.models.query import QuerySet
from django.http import HttpResponse
from openpyxl import Workbook

from application.commons.services.export import export_csv, export_excel
from application.core.models import Observation, Product


def export_observations_excel(product: Product, status: Optional[str]) -> Workbook:
    observations = _get_observations(product, status)
    return export_excel(
        observations, "Observations", _get_excludes(), _get_foreign_keys()
    )


def export_observations_csv(
    response: HttpResponse, product: Product, status: Optional[str]
) -> None:
    observations = _get_observations(product, status)
    export_csv(
        response,
        observations,
        _get_excludes(),
        _get_foreign_keys(),
    )


def _get_observations(product: Product, status: Optional[str]) -> QuerySet:
    if product.is_product_group:
        observations = Observation.objects.filter(product__product_group=product)
    else:
        observations = Observation.objects.filter(product=product)

    if status:
        observations = observations.filter(current_status=status)

    observations = observations.order_by("current_status", "current_severity", "title")

    return observations


def _get_excludes():
    return [
        "identity_hash",
        "pk",
        "objects",
        "unsaved_references",
        "unsaved_evidences",
        "NUMERICAL_SEVERITIES",
        "SEVERITY_CHOICES",
        "SEVERITY_CRITICAL",
        "SEVERITY_HIGH",
        "SEVERITY_LOW",
        "SEVERITY_MEDIUM",
        "SEVERITY_NONE",
        "SEVERITY_UNKOWN",
        "STATUS_CHOICES",
        "STATUS_DUPLICATE",
        "STATUS_FALSE_POSITIVE",
        "STATUS_IN_REVIEW",
        "STATUS_NOT_AFFECTED",
        "STATUS_OPEN",
        "STATUS_RESOLVED",
        "STATUS_RISK_ACCEPTED",
        "STATUS_NOT_SECURITY",
        "origin_service",
    ]


def _get_foreign_keys():
    return ["branch", "parser", "product"]
