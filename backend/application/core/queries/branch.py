from typing import Optional

from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.access_control.services.current_user import get_current_user
from application.core.models import (
    Branch,
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
)


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

    branches = Branch.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(product=OuterRef("product_id"), user=user)
        product_group_members = Product_Member.objects.filter(product=OuterRef("product__product_group"), user=user)

        product_authorization_group_members = Product_Authorization_Group_Member.objects.filter(
            product=OuterRef("product_id"),
            authorization_group__users=user,
        )

        product_group_authorization_group_members = Product_Authorization_Group_Member.objects.filter(
            product=OuterRef("product__product_group"),
            authorization_group__users=user,
        )

        branches = branches.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
            authorization_group_member=Exists(product_authorization_group_members),
            product_group_authorization_group_member=Exists(product_group_authorization_group_members),
        )

        branches = branches.filter(
            Q(product__member=True)
            | Q(product__product_group__member=True)
            | Q(authorization_group_member=True)
            | Q(product_group_authorization_group_member=True)
        )

    return branches


def get_branches_by_product(product: Product) -> QuerySet[Branch]:
    return Branch.objects.filter(product=product)
