from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Potential_Duplicate, Product
from application.core.services.assessment import save_assessment
from application.core.services.potential_duplicates import set_potential_duplicate
from application.core.services.security_gate import check_security_gate
from application.core.types import Status
from application.issue_tracker.services.issue_tracker import (
    push_deleted_observation_to_issue_tracker,
)


def observations_bulk_assessment(
    product: Product,
    new_severity: str,
    new_status: str,
    comment: str,
    observation_ids: list[int],
) -> None:
    observations = _check_observations(product, observation_ids)
    for observation in observations:
        save_assessment(observation, new_severity, new_status, comment)


def observations_bulk_delete(product: Product, observation_ids: list[int]) -> None:
    observations = _check_observations(product, observation_ids)
    issue_ids: list[str] = []
    for observation in observations:
        issue_ids.append(observation.issue_tracker_issue_id)

    observations.delete()

    for issue_id in issue_ids:
        push_deleted_observation_to_issue_tracker(product, issue_id, get_current_user())

    check_security_gate(product)
    product.last_observation_change = timezone.now()
    product.save()


def observations_bulk_mark_duplicates(
    product: Product,
    observation_id: int,
    potential_duplicate_ids: list[int],
) -> None:
    try:
        observation = Observation.objects.get(pk=observation_id)
        if observation.product != product:
            raise ValidationError(
                f"Observation {observation.pk} does not belong to product {product.pk}"
            )
    except Observation.DoesNotExist:
        raise ValidationError(  # pylint: disable=raise-missing-from
            "Observation does not exist"
        )
        # The DoesNotExist exception itself is not relevant and must not be re-raised

    observation_ids = []
    for potential_duplicate_id in potential_duplicate_ids:
        potential_duplicate = Potential_Duplicate.objects.get(id=potential_duplicate_id)
        observation_ids.append(potential_duplicate.potential_duplicate_observation.id)
    duplicates = _check_observations(product, observation_ids)

    if (
        potential_duplicate.type
        == Potential_Duplicate.POTENTIAL_DUPLICATE_TYPE_COMPONENT
    ):
        comment = f"Duplicate of {observation.origin_component_name_version}"
    elif (
        potential_duplicate.type == Potential_Duplicate.POTENTIAL_DUPLICATE_TYPE_SOURCE
    ):
        comment = f"Duplicate of {observation.title} from scanner {observation.scanner}"
    else:
        raise ValidationError("Invalid potential duplicate type")

    for duplicate in duplicates:
        duplicate.has_potential_duplicates = False
        save_assessment(duplicate, None, Status.STATUS_DUPLICATE, comment)

    set_potential_duplicate(observation)


def _check_observations(
    product: Product, observation_ids: list[int]
) -> QuerySet[Observation]:
    observations = Observation.objects.filter(id__in=observation_ids)
    if len(observations) != len(observation_ids):
        raise ValidationError("Some observations do not exist")

    for observation in observations:
        if observation.product != product:
            raise ValidationError(
                f"Observation {observation.pk} does not belong to product {product.pk}"
            )

    return observations
