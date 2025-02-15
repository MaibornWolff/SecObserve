import logging

from django.db import migrations

from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.migration")


def initialize_branches(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")
    Service = apps.get_model("core", "Service")
    for observation in Observation.objects.exclude(origin_service_name=""):
        try:
            try:
                service = Service.objects.get(product=observation.product, name=observation.origin_service_name)
            except Service.DoesNotExist:
                service = Service.objects.create(product=observation.product, name=observation.origin_service_name)
            observation.origin_service = service
            observation.save()
        except Exception as e:
            logger.error(format_log_message(exception=e))


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0023_service_observation_origin_service_and_more"),
    ]

    operations = [
        migrations.RunPython(initialize_branches),
    ]
