import logging
from datetime import date, timedelta
from typing import Optional

from django.core.paginator import Paginator
from django.db import migrations

from application.core.services.risk_acceptance_expiry import (
    calculate_risk_acceptance_expiry_date,
)
from application.core.types import Status

logger = logging.getLogger("secobserve.migration")


def correct_risk_acceptance_expiry_date(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")

    Observation_Log = apps.get_model("core", "Observation_Log")
    observations = Observation.objects.filter(
        current_status=Status.STATUS_RISK_ACCEPTED
    ).order_by("id")

    paginator = Paginator(observations, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for observation in page.object_list:
            risk_acceptance_expiry_date_found = False
            most_recent_risk_acceptance: Optional[date] = None

            observation_logs = Observation_Log.objects.filter(
                observation=observation
            ).order_by("-created")
            for observation_log in observation_logs:
                if (
                    observation_log.status == Status.STATUS_RISK_ACCEPTED
                    and not most_recent_risk_acceptance
                ):
                    most_recent_risk_acceptance = observation_log.created.date()

                if observation_log.risk_acceptance_expiry_date:
                    observation.risk_acceptance_expiry_date = (
                        observation_log.risk_acceptance_expiry_date
                    )
                    risk_acceptance_expiry_date_found = True
                    break

            if (
                not risk_acceptance_expiry_date_found
                and observation.risk_acceptance_expiry_date
            ):
                new_risk_acceptance_expiry_date = calculate_risk_acceptance_expiry_date(
                    observation.product
                )
                if most_recent_risk_acceptance:
                    days_between = (date.today() - most_recent_risk_acceptance).days
                    observation.risk_acceptance_expiry_date = (
                        new_risk_acceptance_expiry_date - timedelta(days=days_between)
                    )
                else:
                    observation.risk_acceptance_expiry_date = (
                        new_risk_acceptance_expiry_date
                    )

            updates.append(observation)

        Observation.objects.bulk_update(updates, ["risk_acceptance_expiry_date"])


class Migration(migrations.Migration):
    dependencies = [
        (
            "core",
            "0055_product_authorization_group_members",
        ),
    ]

    operations = [
        migrations.RunPython(
            correct_risk_acceptance_expiry_date,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
