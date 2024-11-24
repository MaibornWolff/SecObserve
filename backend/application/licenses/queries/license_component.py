from typing import Optional

from django.db.models import Count, Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import (
    Branch,
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
)
from application.licenses.models import License_Component


def get_license_components() -> QuerySet[License_Component]:
    user = get_current_user()

    if user is None:
        return License_Component.objects.none()

    components = License_Component.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("product_id"),
            user=user,
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("product__product_group"),
            user=user,
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("product_id"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("product__product_group"),
                authorization_group__users=user,
            )
        )

        components = components.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
            product__authorization_group_member=Exists(
                product_authorization_group_members
            ),
            product__product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        components = components.filter(
            Q(product__member=True)
            | Q(product__product_group__member=True)
            | Q(product__authorization_group_member=True)
            | Q(product__product_group_authorization_group_member=True)
        )

    return components


def get_license_component_licenses(
    product: Product, branch: Optional[Branch]
) -> QuerySet:
    license_components = get_license_components().filter(
        product=product,
    )
    if branch:
        license_components = license_components.filter(branch=branch)

    return (
        license_components.values(
            "branch__name",
            "license__spdx_id",
            "license__name",
            "unknown_license",
            "evaluation_result",
        )
        .annotate(Count("id"))
        .order_by("numerical_evaluation_result", "license__spdx_id", "unknown_license")
    )
