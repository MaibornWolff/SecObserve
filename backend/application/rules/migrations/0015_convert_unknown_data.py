import logging

from django.core.paginator import Paginator
from django.db import migrations
from django.db.models import Q

logger = logging.getLogger("secobserve.migration")


def convert_unknown_data(apps, schema_editor):
    Rule = apps.get_model("rules", "Rule")
    rules = Rule.objects.filter(new_severity="Unkown").order_by("id")

    paginator = Paginator(rules, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for rule in page.object_list:
            rule.new_severity = "Unknown"
            updates.append(rule)

        Rule.objects.bulk_update(
            updates,
            [
                "new_severity",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "rules",
            "0014_alter_rule_new_severity",
        ),
    ]

    operations = [
        migrations.RunPython(
            convert_unknown_data,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
