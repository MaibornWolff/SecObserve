import logging

from django.core.paginator import Paginator
from django.db import migrations
from django.db.models import Q

logger = logging.getLogger("secobserve.migration")


def convert_unknown_data(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")
    observations = Observation.objects.filter(
        Q(assessment_severity="Unkown")
        | Q(current_severity="Unkown")
        | Q(parser_severity="Unkown")
        | Q(rule_severity="Unkown")
    ).order_by("id")

    paginator = Paginator(observations, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for observation in page.object_list:
            if observation.assessment_severity == "Unkown":
                observation.assessment_severity = "Unknown"
            if observation.current_severity == "Unkown":
                observation.current_severity = "Unknown"
            if observation.parser_severity == "Unkown":
                observation.parser_severity = "Unknown"
            if observation.rule_severity == "Unkown":
                observation.rule_severity = "Unknown"

            updates.append(observation)

        Observation.objects.bulk_update(
            updates,
            [
                "assessment_severity",
                "current_severity",
                "parser_severity",
                "rule_severity",
            ],
        )

    Observation_Log = apps.get_model("core", "Observation_Log")
    observation_logs = Observation_Log.objects.filter(severity="Unkown").order_by("id")

    paginator = Paginator(observation_logs, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for observation_log in page.object_list:
            if observation_log.severity == "Unkown":
                observation_log.severity = "Unknown"

            updates.append(observation_log)

        Observation_Log.objects.bulk_update(
            updates,
            [
                "severity",
            ],
        )

    Product = apps.get_model("core", "Product")
    products = Product.objects.filter(issue_tracker_minimum_severity="Unkown").order_by("id")

    paginator = Paginator(products, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for product in page.object_list:
            if product.issue_tracker_minimum_severity == "Unkown":
                product.issue_tracker_minimum_severity = "Unknown"

            updates.append(product)

        Product.objects.bulk_update(
            updates,
            [
                "issue_tracker_minimum_severity",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "core",
            "0053_rename_security_gate_threshold_unkown_product_security_gate_threshold_unknown_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            convert_unknown_data,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
