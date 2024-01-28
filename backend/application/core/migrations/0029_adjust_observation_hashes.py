import logging

from django.db import migrations

from application.commons.services.log_message import format_log_message
from application.core.services.observation import get_identity_hash

logger = logging.getLogger("secobserve.migration")


def adjust_identity_hashes(apps, schema_editor):
    # Needs to be done because the identity_hash is not based on origin_docker_image_tag anymore
    Observation = apps.get_model("core", "Observation")
    for observation in Observation.objects.exclude(origin_docker_image_name=""):
        try:
            observation.identity_hash = get_identity_hash(observation)
            observation.save()
        except Exception as e:
            logger.error(format_log_message(exception=e))


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0028_product_notification_slack_webhook"),
    ]

    operations = [
        migrations.RunPython(adjust_identity_hashes),
    ]
