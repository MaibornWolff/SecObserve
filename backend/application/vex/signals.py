from typing import Any

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from application.core.models import Observation
from application.vex.models import VEX_Statement
from application.vex.services.vex_engine import write_observation_log_no_vex_statement


@receiver(pre_delete, sender=VEX_Statement)
def vex_statement_pre_delete(  # pylint: disable=unused-argument
    sender: Any, instance: VEX_Statement, **kwargs: Any
) -> None:
    # sender is needed according to Django documentation
    observations = Observation.objects.filter(vex_statement=instance)
    for observation in observations:
        write_observation_log_no_vex_statement(observation, instance)
