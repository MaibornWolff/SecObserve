from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet
from django.utils import timezone

from application.commons.services.global_request import get_current_user
from application.core.models import Product_Member
from application.core.queries.product import get_products
from application.metrics.models import Product_Metrics


def get_product_metrics() -> QuerySet[Product_Metrics]:
    user = get_current_user()

    if user is None:
        return Product_Metrics.objects.none()

    product_metrics = Product_Metrics.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("product__product_group"), user=user
        )

        product_metrics = product_metrics.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
        )

        product_metrics = product_metrics.filter(
            is_product_group=False
            & (Q(product__member=True) | Q(product__product_group__member=True))
        )

    return product_metrics


def get_todays_product_metrics() -> QuerySet[Product_Metrics]:
    return get_product_metrics().filter(date=timezone.localdate())
