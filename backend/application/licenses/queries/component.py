from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import Product_Authorization_Group_Member, Product_Member
from application.licenses.models import Component


def get_components() -> QuerySet[Component]:
    user = get_current_user()

    if user is None:
        return Component.objects.none()

    components = Component.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("component_license__vulnerability_check__product_id"),
            user=user,
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef(
                "component_license__vulnerability_check__product__product_group"
            ),
            user=user,
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("component_license__vulnerability_check__product_id"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef(
                    "component_license__vulnerability_check__product__product_group"
                ),
                authorization_group__users=user,
            )
        )

        components = components.annotate(
            component_license__vulnerability_check__product__member=Exists(
                product_members
            ),
            component_license__vulnerability_check__product__product_group__member=Exists(
                product_group_members
            ),
            component_license__vulnerability_check__product__authorization_group_member=Exists(
                product_authorization_group_members
            ),
            component_license__vulnerability_check__product__product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        components = components.filter(
            Q(component_license__vulnerability_check__product__member=True)
            | Q(
                component_license__vulnerability_check__product__product_group__member=True
            )
            | Q(
                component_license__vulnerability_check__product__authorization_group_member=True
            )
            | Q(
                component_license__vulnerability_check__product__product_group_authorization_group_member=True
            )
        )

    return components
