from application.commons.services.global_request import get_current_user
from application.core.models import Observation
from application.core.services.observation import (
    get_current_severity,
    get_current_status,
)
from application.core.services.observation_log import create_observation_log
from application.core.services.security_gate import check_security_gate
from application.issue_tracker.services.issue_tracker import (
    push_observation_to_issue_tracker,
)


def save_assessment(
    observation: Observation, new_severity: str, new_status: str, comment: str
) -> None:
    previous_severity = observation.current_severity
    previous_assessment_severity = observation.assessment_severity
    log_severity = ""
    if new_severity and new_severity != observation.current_severity:
        observation.assessment_severity = new_severity
        observation.current_severity = get_current_severity(observation)
        log_severity = observation.current_severity

    previous_status = observation.current_status
    previous_assessment_status = observation.assessment_status
    log_status = ""
    if new_status and new_status != observation.current_status:
        observation.assessment_status = new_status
        observation.current_status = get_current_status(observation)
        log_status = observation.current_status

    if (
        previous_severity != observation.current_severity
        or previous_assessment_severity != observation.assessment_severity
        or previous_status != observation.current_status
        or previous_assessment_status != observation.assessment_status
    ):
        observation.save()

    if (
        previous_severity != observation.current_severity
        or previous_status != observation.current_status
    ):
        create_observation_log(observation, log_severity, log_status, comment)

    check_security_gate(observation.product)
    push_observation_to_issue_tracker(observation, get_current_user())


def remove_assessment(observation: Observation, comment: str) -> None:
    if observation.assessment_severity or observation.assessment_status:
        observation.assessment_severity = ""
        observation.assessment_status = ""
        observation.current_severity = get_current_severity(observation)
        observation.current_status = get_current_status(observation)

        create_observation_log(observation, "", "", comment)

        check_security_gate(observation.product)
        push_observation_to_issue_tracker(observation, get_current_user())
