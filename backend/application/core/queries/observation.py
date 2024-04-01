from typing import Optional

from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Observation_Log,
    Potential_Duplicate,
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
)


def get_observation_by_id(observation_id: int) -> Optional[Observation]:
    try:
        return Observation.objects.get(id=observation_id)
    except Observation.DoesNotExist:
        return None


def get_observations() -> QuerySet[Observation]:
    user = get_current_user()

    if user is None:
        return Observation.objects.none()

    observations = Observation.objects.all()

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

        observations = observations.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
            authorization_group_member=Exists(product_authorization_group_members),
            product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        observations = observations.filter(
            Q(product__member=True)
            | Q(product__product_group__member=True)
            | Q(authorization_group_member=True)
            | Q(product_group_authorization_group_member=True)
        )

    return observations


def get_observations_for_vulnerability_check(
    product: Product,
    branch: Optional[Branch],
    filename: str,
    api_configuration_name: str,
) -> QuerySet[Observation]:
    return Observation.objects.filter(
        product=product,
        branch=branch,
        upload_filename=filename,
        api_configuration_name=api_configuration_name,
    )


def get_evidences() -> QuerySet[Evidence]:
    user = get_current_user()

    if user is None:
        return Evidence.objects.none()

    evidences = Evidence.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("observation__product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("observation__product__product_group"), user=user
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("observation__product_id"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("observation__product__product_group"),
                authorization_group__users=user,
            )
        )

        evidences = evidences.annotate(
            observation__product__member=Exists(product_members),
            observation__product__product_group__member=Exists(product_group_members),
            observation__product__authorization_group_member=Exists(
                product_authorization_group_members
            ),
            observation__product__product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        evidences = evidences.filter(
            Q(observation__product__member=True)
            | Q(observation__product__product_group__member=True)
            | Q(observation__product__authorization_group_member=True)
            | Q(observation__product__product_group_authorization_group_member=True)
        )

    return evidences


def get_potential_duplicates() -> QuerySet[Potential_Duplicate]:
    user = get_current_user()

    if user is None:
        return Potential_Duplicate.objects.none()

    potential_duplicates = Potential_Duplicate.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("observation__product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("observation__product__product_group"), user=user
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("observation__product_id"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("observation__product__product_group"),
                authorization_group__users=user,
            )
        )

        potential_duplicates = potential_duplicates.annotate(
            observation__product__member=Exists(product_members),
            observation__product__product_group__member=Exists(product_group_members),
            observation__product__authorization_group_member=Exists(
                product_authorization_group_members
            ),
            observation__product__product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        potential_duplicates = potential_duplicates.filter(
            Q(observation__product__member=True)
            | Q(observation__product__product_group__member=True)
            | Q(observation__product__authorization_group_member=True)
            | Q(observation__product__product_group_authorization_group_member=True)
        )

    return potential_duplicates


def get_observation_log_by_id(observation_log_id: int) -> Optional[Observation_Log]:
    try:
        return Observation_Log.objects.get(id=observation_log_id)
    except Observation_Log.DoesNotExist:
        return None


def get_observation_logs() -> QuerySet[Observation_Log]:
    user = get_current_user()

    if user is None:
        return Observation_Log.objects.none()

    observation_logs = Observation_Log.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("observation__product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("observation__product__product_group"), user=user
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("observation__product_id"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("observation__product__product_group"),
                authorization_group__users=user,
            )
        )

        observation_logs = observation_logs.annotate(
            observation__product__member=Exists(product_members),
            observation__product__product_group__member=Exists(product_group_members),
            observation__product__authorization_group_member=Exists(
                product_authorization_group_members
            ),
            observation__product__product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        observation_logs = observation_logs.filter(
            Q(observation__product__member=True)
            | Q(observation__product__product_group__member=True)
            | Q(observation__product__authorization_group_member=True)
            | Q(observation__product__product_group_authorization_group_member=True)
        )

    return observation_logs


def get_current_observation_log(observation: Observation):
    try:
        return Observation_Log.objects.filter(observation=observation).latest("created")
    except Observation_Log.DoesNotExist:
        return None
