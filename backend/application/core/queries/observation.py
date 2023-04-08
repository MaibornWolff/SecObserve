from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import (
    Observation,
    Product,
    Parser,
    Product_Member,
    Evidence,
)


def get_observation_by_id(id: int) -> Observation:
    try:
        return Observation.objects.get(id=id)
    except Observation.DoesNotExist:
        return None


def get_observations() -> QuerySet[Observation]:
    user = get_current_user()

    if user is None:
        return Observation.objects.none()

    if user.is_superuser:
        return Observation.objects.all()

    product_members = Product_Member.objects.filter(
        product=OuterRef("product_id"), user=user
    )

    return Observation.objects.annotate(product__member=Exists(product_members)).filter(
        product__member=True
    )


def get_observations_for_vulnerability_check(
    product: Product, parser: Parser, filename: str, api_configuration_name: str
) -> QuerySet[Observation]:
    return get_observations().filter(
        product=product,
        parser=parser,
        upload_filename=filename,
        api_configuration_name=api_configuration_name,
    )


def get_evidences() -> QuerySet[Evidence]:
    user = get_current_user()

    if user is None:
        return Evidence.objects.none()

    if user.is_superuser:
        return Evidence.objects.all()

    product_members = Product_Member.objects.filter(
        product=OuterRef("observation__product_id"), user=user
    )

    return Evidence.objects.annotate(
        observation__product__member=Exists(product_members)
    ).filter(observation__product__member=True)
