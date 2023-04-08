from application.core.models import Observation, Observation_Log
from application.commons.services.global_request import get_current_user


def create_observation_log(
    observation: Observation, severity: str, status: str, comment: str
) -> Observation_Log:
    observation_log = Observation_Log(
        observation=observation,
        user=get_current_user(),
        severity=severity,
        status=status,
        comment=comment,
    )
    observation_log.save()
    observation.last_observation_log = observation_log.created
    observation.save()

    return observation_log
