import logging

from django.core.paginator import Paginator
from django.db import migrations

logger = logging.getLogger("secobserve.migration")


def populate_product_flags(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    Observation = apps.get_model("core", "Observation")

    products = Product.objects.filter(is_product_group=False).order_by("id")

    paginator = Paginator(products, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for product in page.object_list:
            product.has_cloud_resource = (
                Observation.objects.filter(product=product).exclude(origin_cloud_qualified_resource="").exists()
            )

            product.has_component = (
                Observation.objects.filter(product=product).exclude(origin_component_name_version="").exists()
            )

            product.has_docker_image = (
                Observation.objects.filter(product=product).exclude(origin_docker_image_name_tag_short="").exists()
            )

            product.has_endpoint = (
                Observation.objects.filter(product=product).exclude(origin_endpoint_hostname="").exists()
            )

            product.has_source = Observation.objects.filter(product=product).exclude(origin_source_file="").exists()

            product.has_potential_duplicates = Observation.objects.filter(
                product=product, has_potential_duplicates=True
            ).exists()

            updates.append(product)

        Product.objects.bulk_update(
            updates,
            [
                "has_cloud_resource",
                "has_component",
                "has_docker_image",
                "has_endpoint",
                "has_source",
                "has_potential_duplicates",
            ],
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0047_product_has_cloud_resource_product_has_component_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_product_flags, reverse_code=migrations.RunPython.noop),
    ]
