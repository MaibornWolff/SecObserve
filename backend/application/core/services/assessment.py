from datetime import date
from typing import Optional

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Observation_Log, Product
from application.core.services.observation import (
    get_current_severity,
    get_current_status,
    get_current_vex_justification,
)
from application.core.services.observation_log import create_observation_log
from application.core.services.risk_acceptance_expiry import (
    calculate_risk_acceptance_expiry_date,
)
from application.core.services.security_gate import check_security_gate
from application.core.types import Assessment_Status, Status
from application.issue_tracker.services.issue_tracker import (
    push_observation_to_issue_tracker,
)


def save_assessment(
    observation: Observation,
    new_severity: Optional[str],
    new_status: Optional[str],
    comment: str,
    new_vex_justification: Optional[str],
    new_risk_acceptance_expiry_date: Optional[date],
) -> None:

    log_severity = (
        new_severity
        if new_severity and new_severity != observation.current_severity
        else ""
    )
    log_status = (
        new_status if new_status and new_status != observation.current_status else ""
    )
    log_vex_justification = (
        new_vex_justification
        if new_vex_justification
        and new_vex_justification != observation.current_vex_justification
        else ""
    )
    log_risk_acceptance_expiry_date = (
        new_risk_acceptance_expiry_date
        if new_risk_acceptance_expiry_date
        and new_risk_acceptance_expiry_date != observation.risk_acceptance_expiry_date
        else None
    )

    assessment_status = (
        Assessment_Status.ASSESSMENT_STATUS_NEEDS_APPROVAL
        if _get_assessments_need_approval(observation.product)
        and (
            (log_severity and log_severity != observation.current_severity)
            or (log_status and log_status != observation.current_status)
            or (
                log_vex_justification
                and log_vex_justification != observation.current_vex_justification
            )
        )
        and new_status != Status.STATUS_IN_REVIEW
        else Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED
    )

    if assessment_status in (
        Assessment_Status.ASSESSMENT_STATUS_APPROVED,
        Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
    ):
        _update_observation(
            observation,
            new_severity,
            new_status,
            new_vex_justification,
            new_risk_acceptance_expiry_date,
        )

        create_observation_log(
            observation,
            log_severity,
            log_status,
            comment,
            log_vex_justification,
            assessment_status,
            log_risk_acceptance_expiry_date,
        )

        check_security_gate(observation.product)
        push_observation_to_issue_tracker(observation, get_current_user())
    else:
        create_observation_log(
            observation,
            log_severity,
            log_status,
            comment,
            log_vex_justification,
            assessment_status,
            log_risk_acceptance_expiry_date,
        )


def _update_observation(
    observation: Observation,
    new_severity: Optional[str],
    new_status: Optional[str],
    new_vex_justification: Optional[str],
    new_risk_acceptance_expiry_date: Optional[date],
) -> None:
    previous_current_severity = observation.current_severity
    previous_assessment_severity = observation.assessment_severity
    if new_severity and new_severity != observation.current_severity:
        observation.assessment_severity = new_severity
        observation.current_severity = get_current_severity(observation)

    previous_current_status = observation.current_status
    previous_assessment_status = observation.assessment_status
    if new_status and new_status != observation.current_status:
        observation.assessment_status = new_status
        observation.current_status = get_current_status(observation)

    previous_current_vex_justification = observation.current_vex_justification
    previous_assessment_vex_justification = observation.assessment_vex_justification
    if (
        new_vex_justification
        and new_vex_justification != observation.current_vex_justification
    ):
        observation.assessment_vex_justification = new_vex_justification
        observation.current_vex_justification = get_current_vex_justification(
            observation
        )

    previous_risk_acceptance_expiry_date = observation.risk_acceptance_expiry_date
    observation.risk_acceptance_expiry_date = new_risk_acceptance_expiry_date

    if (
        previous_current_severity  # pylint: disable=too-many-boolean-expressions
        != observation.current_severity
        or previous_assessment_severity != observation.assessment_severity
        or previous_current_status != observation.current_status
        or previous_assessment_status != observation.assessment_status
        or previous_current_vex_justification != observation.current_vex_justification
        or previous_assessment_vex_justification
        != observation.assessment_vex_justification
        or previous_risk_acceptance_expiry_date
        != observation.risk_acceptance_expiry_date
    ):
        observation.save()


def _get_assessments_need_approval(product: Product) -> bool:
    if product.product_group and product.product_group.assessments_need_approval:
        return True
    return product.assessments_need_approval


def remove_assessment(observation: Observation, comment: str) -> bool:
    if observation.assessment_severity or observation.assessment_status:
        observation.assessment_severity = ""
        observation.assessment_status = ""
        observation.assessment_vex_justification = ""
        observation.current_severity = get_current_severity(observation)
        observation.current_status = get_current_status(observation)
        observation.current_vex_justification = get_current_vex_justification(
            observation
        )
        risk_acceptance_expiry_date = (
            calculate_risk_acceptance_expiry_date(observation.product)
            if observation.current_status == Status.STATUS_RISK_ACCEPTED
            else None
        )
        observation.risk_acceptance_expiry_date = risk_acceptance_expiry_date

        create_observation_log(
            observation,
            "",
            "",
            comment,
            "",
            Assessment_Status.ASSESSMENT_STATUS_REMOVED,
            risk_acceptance_expiry_date,
        )

        check_security_gate(observation.product)
        push_observation_to_issue_tracker(observation, get_current_user())

        return True

    return False


def assessment_approval(
    observation_log: Observation_Log, assessment_status: str, approval_remark: str
) -> None:
    if (
        observation_log.assessment_status
        != Assessment_Status.ASSESSMENT_STATUS_NEEDS_APPROVAL
    ):
        raise ValidationError("Observation log does not need approval")

    approval_user = get_current_user()
    if observation_log.user == approval_user:
        raise ValidationError("Users cannot approve their own assessment")

    if assessment_status in (
        Assessment_Status.ASSESSMENT_STATUS_APPROVED,
        Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
    ):
        _update_observation(
            observation_log.observation,
            observation_log.severity,
            observation_log.status,
            observation_log.vex_justification,
            observation_log.risk_acceptance_expiry_date,
        )

        check_security_gate(observation_log.observation.product)
        push_observation_to_issue_tracker(
            observation_log.observation, get_current_user()
        )

    observation_log.approval_user = approval_user
    observation_log.approval_remark = approval_remark
    observation_log.approval_date = timezone.now()
    observation_log.assessment_status = assessment_status
    observation_log.save()
