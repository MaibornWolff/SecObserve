from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Product
from application.core.services.assessment import save_assessment
from application.core.services.security_gate import check_security_gate
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
