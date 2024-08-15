import logging

from django.db import migrations

from application.core.services.observation import normalize_origin_component

logger = logging.getLogger("secobserve.migration")


def populate_purl_type(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")
    for observation in Observation.objects.exclude(origin_component_purl="").filter(
        origin_component_purl_type=""
    ):
        normalize_origin_component(observation)
        observation.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0044_observation_purl_type"),
    ]

    operations = [
        migrations.RunPython(populate_purl_type),
    ]
