import logging

from django.core.paginator import Paginator
from django.db import migrations
from django.db.models import Q

logger = logging.getLogger("secobserve.migration")


def convert_unknown_data(apps, schema_editor):
    Parser = apps.get_model("import_observations", "Parser")
    parsers = Parser.objects.filter(source="Unkown").order_by("id")

    paginator = Paginator(parsers, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for parser in page.object_list:
            parser.source = "Unknown"
            updates.append(parser)

        Parser.objects.bulk_update(
            updates,
            [
                "source",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "import_observations",
            "0008_alter_parser_source",
        ),
    ]

    operations = [
        migrations.RunPython(
            convert_unknown_data,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
