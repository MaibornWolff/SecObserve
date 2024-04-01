from typing import Optional

from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import (
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
)


def get_product_by_id(
    product_id: int, is_product_group: bool = None
) -> Optional[Product]:
    try:
        if is_product_group is None:
            return Product.objects.get(id=product_id)
        return Product.objects.get(id=product_id, is_product_group=is_product_group)
    except Product.DoesNotExist:
        return None


def get_product_by_name(name: str, is_product_group: bool = None) -> Optional[Product]:
    try:
        if is_product_group is None:
            return Product.objects.get(name=name)
        return Product.objects.get(name=name, is_product_group=is_product_group)
    except Product.DoesNotExist:
        return None


def get_products(is_product_group: bool = None) -> QuerySet[Product]:
    user = get_current_user()

    if user is None:
        return Product.objects.none()

    products = Product.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("pk"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("product_group"), user=user
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("pk"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("product_group"),
                authorization_group__users=user,
            )
        )

        products = products.annotate(
            member=Exists(product_members),
            product_group_member=Exists(product_group_members),
            authorization_group_member=Exists(product_authorization_group_members),
            product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )
        products = products.filter(
            Q(member=True)
            | Q(product_group_member=True)
            | Q(authorization_group_member=True)
            | Q(product_group_authorization_group_member=True)
        )

    if is_product_group is not None:
        products = products.filter(is_product_group=is_product_group)

    return products
