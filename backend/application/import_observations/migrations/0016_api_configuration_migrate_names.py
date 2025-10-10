import logging

from django.core.paginator import Paginator
from django.db import migrations
from django.db.models import Q

logger = logging.getLogger("secobserve.migration")


def migrate_service_names(apps, schema_editor):
    API_Configuration = apps.get_model("import_observations", "API_Configuration")
    Service = apps.get_model("core", "Service")

    api_configurations = API_Configuration.objects.exclude(automatic_import_service_legacy__exact="").order_by("id")

    paginator = Paginator(api_configurations, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for api_configuration in page.object_list:
            service = Service.objects.filter(
                product=api_configuration.product, name=api_configuration.automatic_import_service_legacy
            ).first()
            if service:
                api_configuration.automatic_import_service = service
                api_configuration.automatic_import_service_legacy = ""
                updates.append(api_configuration)

        API_Configuration.objects.bulk_update(
            updates,
            [
                "automatic_import_service",
                "automatic_import_service_legacy",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "import_observations",
            "0015_api_configuration_automatic_import_service",
        ),
    ]

    operations = [
        migrations.RunPython(
            migrate_service_names,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
