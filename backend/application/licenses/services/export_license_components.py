from django.db.models.query import QuerySet
from django.http import HttpResponse
from openpyxl import Workbook

from application.commons.services.export import export_csv, export_excel
from application.core.models import Product
from application.licenses.models import License_Component


def export_license_components_excel(product: Product) -> Workbook:
    license_components = _get_license_components(product)
    return export_excel(
        license_components, "License Components", _get_excludes(), _get_foreign_keys()
    )


def export_license_components_csv(response: HttpResponse, product: Product) -> None:
    license_components = _get_license_components(product)
    export_csv(
        response,
        license_components,
        _get_excludes(),
        _get_foreign_keys(),
    )


def _get_license_components(product: Product) -> QuerySet:
    if product.is_product_group:
        license_components = License_Component.objects.filter(
            product__product_group=product
        )
    else:
        license_components = License_Component.objects.filter(product=product)

    license_components = license_components.order_by(
        "numerical_evaluation_result",
        "license__name",
        "unknown_license",
        "name_version",
    )

    return license_components


def _get_excludes():
    return [
        "identity_hash",
        "pk",
        "objects",
        "unsaved_license",
    ]


def _get_foreign_keys():
    return ["branch", "license", "product"]
