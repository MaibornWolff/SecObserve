from django.core.paginator import Paginator
from django.db import migrations

from application.licenses.services.license_component import get_identity_hash


def initialize_effective_licenses(apps, schema_editor):
    License_Component = apps.get_model("licenses", "License_Component")
    license_components = License_Component.objects.all().order_by("id")

    paginator = Paginator(license_components, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for license_component in page.object_list:
            license_component.identity_hash = get_identity_hash(license_component)

            license_component.effective_license_name = license_component.imported_declared_license_name
            license_component.effective_spdx_license = license_component.imported_declared_spdx_license
            license_component.effective_license_expression = license_component.imported_declared_license_expression
            license_component.effective_non_spdx_license = license_component.imported_declared_non_spdx_license
            license_component.effective_multiple_licenses = license_component.imported_declared_multiple_licenses

            updates.append(license_component)

        License_Component.objects.bulk_update(
            updates,
            [
                "identity_hash",
                "effective_license_name",
                "effective_spdx_license",
                "effective_license_expression",
                "effective_non_spdx_license",
                "effective_multiple_licenses",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "licenses",
            "0018_rename_license_license_component_declared_license_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            initialize_effective_licenses,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
