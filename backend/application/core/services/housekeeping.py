import logging
import re
from datetime import timedelta

from django.utils import timezone

from application.commons.models import Settings
from application.core.models import Branch, Observation, Product

logger = logging.getLogger("secobserve.core")


def delete_inactive_branches_and_set_flags() -> None:
    products = Product.objects.filter(is_product_group=False)
    for product in products:
        delete_inactive_branches_for_product(product)
        set_product_flags(product)


def delete_inactive_branches_for_product(product: Product) -> None:
    product_group_specific = False
    keep_inactive_days = None
    exempt_branches = None
    if product.product_group:
        product_group: Product = product.product_group
        if product_group.repository_branch_housekeeping_active is False:
            # Branch housekeeping is disabled for this product group
            return
        if product_group.repository_branch_housekeeping_active is True:
            # Branch housekeeping is product group specific
            product_group_specific = True
            keep_inactive_days = product_group.repository_branch_housekeeping_keep_inactive_days
            exempt_branches = product_group.repository_branch_housekeeping_exempt_branches

    if not product_group_specific:
        if product.repository_branch_housekeeping_active is False:
            # Branch housekeeping is disabled for this product
            return

        if product.repository_branch_housekeeping_active is True:
            # Branch housekeeping is product specific
            keep_inactive_days = product.repository_branch_housekeeping_keep_inactive_days
            exempt_branches = product.repository_branch_housekeeping_exempt_branches
        else:
            settings = Settings.load()

            # Branch housekeeping is standard
            if not settings.branch_housekeeping_active:
                # Branch housekeeping is disabled
                return

            keep_inactive_days = settings.branch_housekeeping_keep_inactive_days
            exempt_branches = settings.branch_housekeeping_exempt_branches

    if not keep_inactive_days:
        # Branch housekeeping has no inactive days configured
        return

    inactive_date = timezone.now() - timedelta(days=keep_inactive_days)

    compiled_exempt_branches = None
    if exempt_branches:
        compiled_exempt_branches = re.compile(exempt_branches, re.IGNORECASE)

    branches = Branch.objects.filter(product=product, housekeeping_protect=False, last_import__lte=inactive_date)

    for branch in branches:
        if product.repository_default_branch == branch or (
            compiled_exempt_branches and compiled_exempt_branches.match(branch.name)
        ):
            continue

        logger.info(  # pylint: disable=logging-fstring-interpolation
            f"Deleting branch {branch.name} for product {product.name}"
        )
        branch.delete()


def set_product_flags(product: Product) -> None:
    has_cloud_resource_before = product.has_cloud_resource
    product.has_cloud_resource = (
        Observation.objects.filter(product=product).exclude(origin_cloud_qualified_resource="").exists()
    )

    has_component_before = product.has_component
    product.has_component = (
        Observation.objects.filter(product=product).exclude(origin_component_name_version="").exists()
    )

    has_docker_image_before = product.has_docker_image
    product.has_docker_image = (
        Observation.objects.filter(product=product).exclude(origin_docker_image_name_tag_short="").exists()
    )

    has_endpoint_before = product.has_endpoint
    product.has_endpoint = Observation.objects.filter(product=product).exclude(origin_endpoint_hostname="").exists()

    has_kubernetes_resource_before = product.has_kubernetes_resource
    product.has_kubernetes_resource = (
        Observation.objects.filter(product=product).exclude(origin_kubernetes_qualified_resource="").exists()
    )

    has_source_before = product.has_source
    product.has_source = Observation.objects.filter(product=product).exclude(origin_source_file="").exists()

    has_potential_duplicates_before = product.has_potential_duplicates
    product.has_potential_duplicates = Observation.objects.filter(
        product=product, has_potential_duplicates=True
    ).exists()

    if (
        has_cloud_resource_before != product.has_cloud_resource  # pylint: disable=too-many-boolean-expressions
        or has_component_before != product.has_component
        or has_docker_image_before != product.has_docker_image
        or has_endpoint_before != product.has_endpoint
        or has_kubernetes_resource_before != product.has_kubernetes_resource
        or has_source_before != product.has_source
        or has_potential_duplicates_before != product.has_potential_duplicates
    ):
        product.save()
