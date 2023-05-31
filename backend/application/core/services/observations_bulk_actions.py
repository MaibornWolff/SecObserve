from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from application.core.models import Observation, Product
from application.core.services.assessment import save_assessment


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
    observations.delete()


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
