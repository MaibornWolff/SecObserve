from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Observation_Log


def create_observation_log(
    observation: Observation,
    severity: str,
    status: str,
    comment: str,
    vex_justification: str,
    assessment_status: str,
) -> Observation_Log:
    observation_log = Observation_Log(
        observation=observation,
        user=get_current_user(),
        severity=severity,
        status=status,
        comment=comment,
        vex_justification=vex_justification,
        assessment_status=assessment_status,
        general_rule=observation.general_rule,
        product_rule=observation.product_rule,
        vex_statement=observation.vex_statement,
    )
    observation_log.save()
    observation.last_observation_log = observation_log.created
    observation.save()
    observation.product.last_observation_change = observation_log.created
    observation.product.save()

    return observation_log
