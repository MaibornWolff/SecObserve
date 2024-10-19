from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import Product_Authorization_Group_Member, Product_Member
from application.licenses.models import Component_License


def get_component_licenses() -> QuerySet[Component_License]:
    user = get_current_user()

    if user is None:
        return Component_License.objects.none()

    component_licenses = Component_License.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("vulnerability_check__product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("vulnerability_check__product__product_group"), user=user
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("vulnerability_check__product_id"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("vulnerability_check__product__product_group"),
                authorization_group__users=user,
            )
        )

        component_licenses = component_licenses.annotate(
            vulnerability_check__product__member=Exists(product_members),
            vulnerability_check__product__product_group__member=Exists(
                product_group_members
            ),
            vulnerability_check__product__authorization_group_member=Exists(
                product_authorization_group_members
            ),
            vulnerability_check__product__product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        component_licenses = component_licenses.filter(
            Q(vulnerability_check__product__member=True)
            | Q(vulnerability_check__product__product_group__member=True)
            | Q(vulnerability_check__product__authorization_group_member=True)
            | Q(
                vulnerability_check__product__product_group_authorization_group_member=True
            )
        )

    return component_licenses
