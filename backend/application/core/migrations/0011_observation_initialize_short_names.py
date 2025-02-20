from django.db import migrations

from application.core.services.observation import normalize_observation_fields


def touch_observations(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")
    for observation in Observation.objects.all():
        if observation.origin_docker_image_name_tag:
            origin_docker_image_name_tag_parts = observation.origin_docker_image_name_tag.split("/")
            observation.origin_docker_image_name_tag_short = origin_docker_image_name_tag_parts[
                len(origin_docker_image_name_tag_parts) - 1
            ].strip()
        else:
            observation.origin_docker_image_name_tag_short = ""

        observation.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_observation_short_names"),
    ]

    operations = [
        migrations.RunPython(touch_observations),
    ]
