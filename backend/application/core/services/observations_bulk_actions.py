from datetime import date
from typing import Optional

from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError

from application.access_control.services.authorization import (
    user_has_permission,
    user_has_permission_or_403,
)
from application.access_control.services.roles_permissions import Permissions
from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Potential_Duplicate, Product
from application.core.queries.observation import (
    get_current_observation_log,
    get_observation_log_by_id,
)
from application.core.services.assessment import assessment_approval, save_assessment
from application.core.services.potential_duplicates import (
    set_potential_duplicate,
    set_potential_duplicate_both_ways,
)
from application.core.services.security_gate import check_security_gate
from application.core.types import Assessment_Status, Status
from application.issue_tracker.services.issue_tracker import (
    push_deleted_observation_to_issue_tracker,
)


def observations_bulk_assessment(
    *,
    product: Optional[Product],
    new_severity: str,
    new_status: str,
    comment: str,
    observation_ids: list[int],
    new_vex_justification: str,
    new_risk_acceptance_expiry_date: Optional[date],
) -> None:
    observations = _check_observations(product, observation_ids)
    for observation in observations:
        save_assessment(
            observation=observation,
            new_severity=new_severity,
            new_status=new_status,
            comment=comment,
            new_vex_justification=new_vex_justification,
            new_risk_acceptance_expiry_date=new_risk_acceptance_expiry_date,
        )


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
        save_assessment(
            observation=duplicate,
            new_severity=None,
            new_status=Status.STATUS_DUPLICATE,
            comment=comment,
            new_vex_justification="",
            new_risk_acceptance_expiry_date=None,
        )

    set_potential_duplicate(observation)


def _check_observations(
    product: Optional[Product], observation_ids: list[int]
) -> QuerySet[Observation]:
    observations = Observation.objects.filter(id__in=observation_ids)
    if len(observations) != len(observation_ids):
        raise ValidationError("Some observations do not exist")

    for observation in observations:
        if product:
            if observation.product != product:
                raise ValidationError(
                    f"Observation {observation.pk} does not belong to product {product.pk}"
                )
        else:
            if not user_has_permission(observation, Permissions.Observation_Assessment):
                raise ValidationError(
                    f"First observation without assessment permission: {observation}"
                )

        current_observation_log = get_current_observation_log(observation)
        if (
            current_observation_log
            and current_observation_log.assessment_status
            == Assessment_Status.ASSESSMENT_STATUS_NEEDS_APPROVAL
        ):
            raise ValidationError(
                "Cannot create new assessment while last assessment still needs approval"
            )

    return observations


def observation_logs_bulk_approval(
    assessment_status: str,
    approval_remark: str,
    observation_logs: list[int],
) -> None:
    for observation_log_id in observation_logs:
        observation_log = get_observation_log_by_id(observation_log_id)
        if not observation_log:
            raise NotFound(f"Observation Log {observation_log_id} not found")

        user_has_permission_or_403(
            observation_log, Permissions.Observation_Log_Approval
        )

        assessment_approval(observation_log, assessment_status, approval_remark)

        set_potential_duplicate_both_ways(observation_log.observation)
