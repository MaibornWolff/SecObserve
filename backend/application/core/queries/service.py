from typing import Optional

from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import (
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
    Service,
)


def get_service_by_id(product: Product, service_id: int) -> Optional[Service]:
    try:
        return Service.objects.get(id=service_id, product=product)
    except Service.DoesNotExist:
        return None


def get_service_by_name(product: Product, name: str) -> Optional[Service]:
    try:
        return Service.objects.get(name=name, product=product)
    except Service.DoesNotExist:
        return None


def get_services() -> QuerySet[Service]:
    user = get_current_user()

    if user is None:
        return Service.objects.none()

    services = Service.objects.all()

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

        services = services.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
            authorization_group_member=Exists(product_authorization_group_members),
            product_group_authorization_group_member=Exists(product_group_authorization_group_members),
        )

        services = services.filter(
            Q(product__member=True)
            | Q(product__product_group__member=True)
            | Q(authorization_group_member=True)
            | Q(product_group_authorization_group_member=True)
        )

    return services


def get_services_by_product(product: Product) -> QuerySet[Service]:
    return Service.objects.filter(product=product)
