import logging

from django.db import migrations

from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.migration")


def update_last_observation_log(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")
    Observation_Log = apps.get_model("core", "Observation_Log")
    for observation in Observation.objects.all():
        try:
            observation_log = Observation_Log.objects.filter(observation=observation).latest("created")
            observation.last_observation_log = observation_log.created
            observation.save()
        except Exception as e:
            logger.warn(format_log_message(exception=e))


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_observation_last_observation_log"),
    ]

    operations = [
        migrations.RunPython(update_last_observation_log),
    ]
