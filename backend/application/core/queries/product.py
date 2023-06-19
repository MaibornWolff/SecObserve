from typing import Optional

from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet

from application.access_control.models import User
from application.commons.services.global_request import get_current_user
from application.core.models import Branch, Product, Product_Member


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

    product_members = Product_Member.objects.exclude(
        user__username__startswith="-product-"
    )

    if user.is_superuser:
        return product_members

    products = get_products()
    return product_members.filter(product__in=products)


def get_branch_by_id(product: Product, branch_id: int) -> Optional[Branch]:
    try:
        return Branch.objects.get(id=branch_id, product=product)
    except Branch.DoesNotExist:
        return None


def get_branch_by_name(product: Product, name: str) -> Optional[Branch]:
    try:
        return Branch.objects.get(name=name, product=product)
    except Branch.DoesNotExist:
        return None


def get_branches() -> QuerySet[Branch]:
    user = get_current_user()

    if user is None:
        return Branch.objects.none()

    if user.is_superuser:
        return Branch.objects.all()

    products = get_products()
    return Branch.objects.filter(product__in=products)


def get_branches_by_product(product: Product) -> QuerySet[Branch]:
    return Branch.objects.filter(product=product)
