from django.core.paginator import Paginator
from django.db import migrations


def update_license_names(apps, schema_editor):
    License_Component = apps.get_model("licenses", "License_Component")
    license_components = License_Component.objects.all().order_by("id")

    paginator = Paginator(license_components, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for license_component in page.object_list:
            if license_component.license:
                license_component.license_name = license_component.license.spdx_id
            elif license_component.license_expression:
                license_component.license_name = license_component.license_expression
            elif license_component.unknown_license:
                license_component.license_name = license_component.unknown_license
            else:
                license_component.license_name = "No license information"

            updates.append(license_component)

        License_Component.objects.bulk_update(
            updates,
            [
                "license_name",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "licenses",
            "0011_update_license_names",
        ),
    ]

    operations = [
        migrations.RunPython(
            update_license_names,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
