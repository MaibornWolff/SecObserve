from typing import Optional

from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import Product, Product_Member
from application.import_observations.models import Api_Configuration


def get_api_configuration_by_id(
    api_configuration_id: int,
) -> Optional[Api_Configuration]:
    try:
        return Api_Configuration.objects.get(id=api_configuration_id)
    except Api_Configuration.DoesNotExist:
        return None


def get_api_configuration_by_name(
    product: Product, name: str
) -> Optional[Api_Configuration]:
    try:
        return Api_Configuration.objects.get(product=product, name=name)
    except Api_Configuration.DoesNotExist:
        return None


def get_api_configurations() -> QuerySet[Api_Configuration]:
    user = get_current_user()

    if user is None:
        return Api_Configuration.objects.none()

    if user.is_superuser:
        return Api_Configuration.objects.all()

    product_members = Product_Member.objects.filter(
        product=OuterRef("product_id"), user=user
    )

    return Api_Configuration.objects.annotate(
        product__member=Exists(product_members)
    ).filter(product__member=True)
