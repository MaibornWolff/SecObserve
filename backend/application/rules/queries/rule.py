from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import Product_Authorization_Group_Member, Product_Member
from application.rules.models import Rule


def get_general_rules() -> QuerySet[Rule]:
    return Rule.objects.filter(product__isnull=True)


def get_product_rules() -> QuerySet[Rule]:
    user = get_current_user()

    if user is None:
        return Rule.objects.none()

    product_rules = Rule.objects.filter(product__isnull=False)

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("product__product_group"), user=user
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

        product_rules = product_rules.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
            authorization_group_member=Exists(product_authorization_group_members),
            product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        product_rules = product_rules.filter(
            Q(product__member=True)
            | Q(product__product_group__member=True)
            | Q(authorization_group_member=True)
            | Q(product_group_authorization_group_member=True)
        )

    return product_rules
