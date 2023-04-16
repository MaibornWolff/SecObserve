from typing import Optional

from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet

from application.access_control.models import User
from application.commons.services.global_request import get_current_user
from application.core.models import Product, Product_Member


def get_product_by_id(product_id: int) -> Optional[Product]:
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None


def get_product_by_name(name: str) -> Optional[Product]:
    try:
        return Product.objects.get(name=name)
    except Product.DoesNotExist:
        return None


def get_products() -> QuerySet[Product]:
    user = get_current_user()

    if user is None:
        return Product.objects.none()

    if user.is_superuser:
        return Product.objects.all()

    product_members = Product_Member.objects.filter(product=OuterRef("pk"), user=user)
    return Product.objects.annotate(member=Exists(product_members)).filter(member=True)


def get_product_member(product: Product, user: User = None) -> Optional[Product_Member]:
    if not user:
        user = get_current_user()

    try:
        return Product_Member.objects.get(product=product, user=user)
    except Product_Member.DoesNotExist:
        return None


def get_product_members() -> QuerySet[Product_Member]:
    user = get_current_user()

    if user is None:
        return Product_Member.objects.none()

    if user.is_superuser:
        return Product_Member.objects.all()

    products = get_products()
    return Product_Member.objects.filter(product__in=products)
