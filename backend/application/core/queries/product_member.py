from typing import Optional

from django.db.models.query import QuerySet

from application.access_control.models import User
from application.commons.services.global_request import get_current_user
from application.core.models import Product, Product_Member
from application.core.queries.product import get_products


def get_product_member(product: Product, user: User = None) -> Optional[Product_Member]:
    if not user:
        user = get_current_user()

    try:
        return Product_Member.objects.get(product=product, user=user)
    except Product_Member.DoesNotExist:
        if product.product_group:
            return get_product_member(product.product_group, user)
        return None


def get_product_members() -> QuerySet[Product_Member]:
    user = get_current_user()

    if user is None:
        return Product_Member.objects.none()

    product_members = Product_Member.objects.exclude(
        user__username__startswith="-product-"
    )

    if user.is_superuser:
        return product_members

    products = get_products()
    return product_members.filter(product__in=products)
