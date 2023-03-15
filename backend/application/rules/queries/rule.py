from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import Product_Member
from application.rules.models import Rule


def get_general_rules() -> QuerySet[Rule]:
    return Rule.objects.filter(product__isnull=True)


def get_product_rules() -> QuerySet[Rule]:
    user = get_current_user()

    if user is None:
        return Rule.objects.none()

    if user.is_superuser:
        return Rule.objects.filter(product__isnull=False)

    product_members = Product_Member.objects.filter(
        product=OuterRef("product_id"), user=user
    )

    product_rules = Rule.objects.annotate(
        product__member=Exists(product_members)
    ).filter(product__member=True)

    return product_rules
