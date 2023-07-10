from datetime import date

from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.queries.product import get_products
from application.metrics.models import Product_Metrics


def get_product_metrics() -> QuerySet[Product_Metrics]:
    user = get_current_user()

    if user is None:
        return Product_Metrics.objects.none()

    if user.is_superuser:
        return Product_Metrics.objects.all()

    products = get_products()

    return Product_Metrics.objects.filter(product__in=products)


def get_todays_product_metrics() -> QuerySet[Product_Metrics]:
    return get_product_metrics().filter(date=date.today())
