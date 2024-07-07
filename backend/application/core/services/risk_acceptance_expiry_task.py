from datetime import date

from application.core.models import Observation
from application.core.services.assessment import remove_assessment, save_assessment
from application.core.types import Status


def expire_risk_acceptances() -> None:
    observations = Observation.objects.filter(
        current_status=Status.STATUS_RISK_ACCEPTED,
        risk_acceptance_expiry_date__lte=date.today(),
    )
    for observation in observations:
        assessment_removed = remove_assessment(
            observation, "Risk acceptance has expired."
        )
        if not assessment_removed:
            observation.parser_status = Status.STATUS_OPEN
            observation.risk_acceptance_expiry_date = None
            observation.save()
            save_assessment(
                observation,
                "",
                Status.STATUS_OPEN,
                "Risk acceptance has expired.",
                "",
                None,
            )
