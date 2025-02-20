import logging

from django.core.paginator import Paginator
from django.db import migrations

from application.import_observations.parsers.cyclone_dx.dependencies import (
    _generate_dependency_list_as_text,
    _parse_mermaid_graph_content,
)

logger = logging.getLogger("secobserve.migration")


def convert_origin_component_dependencies(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")

    observations = Observation.objects.exclude(origin_component_dependencies="").order_by("id")

    paginator = Paginator(observations, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for observation in page.object_list:
            dependencies = observation.origin_component_dependencies.split("\n")
            # remove duplicates in dependencies while preserving order
            dependencies = list(dict.fromkeys(dependencies))

            mermaid_dependencies = _parse_mermaid_graph_content(dependencies)
            observation.origin_component_dependencies = _generate_dependency_list_as_text(mermaid_dependencies)

            updates.append(observation)

        Observation.objects.bulk_update(
            updates,
            [
                "origin_component_dependencies",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0050_alter_observation_origin_component_dependencies"),
    ]

    operations = [
        migrations.RunPython(
            convert_origin_component_dependencies,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
