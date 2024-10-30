from django.utils import timezone

from application.core.models import Product
from application.licenses.models import (
    License_Component,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.types import License_Policy_Evaluation_Result


def get_license_evaluation_results(product: Product) -> dict:
    if product.license_policy:
        license_policy = product.license_policy
    elif product.product_group and product.product_group.license_policy:
        license_policy = product.product_group.license_policy
    else:
        return {}

    license_evaluation_results = {}

    items_license_groups = License_Policy_Item.objects.filter(
        license_policy=license_policy, license_group__isnull=False
    )
    for item in items_license_groups:
        if item.license_group:
            for my_license in item.license_group.licenses.all():
                license_evaluation_results[f"spdx_{my_license.spdx_id}"] = (
                    item.evaluation_result
                )

    items_licenses = License_Policy_Item.objects.filter(
        license_policy=license_policy, license__isnull=False
    )
    for item in items_licenses:
        if item.license:
            license_evaluation_results[f"spdx_{item.license.spdx_id}"] = (
                item.evaluation_result
            )

    items_unknown_licenses = License_Policy_Item.objects.filter(
        license_policy=license_policy
    ).exclude(unknown_license="")
    for item in items_unknown_licenses:
        license_evaluation_results[f"unknown_{item.unknown_license}"] = (
            item.evaluation_result
        )

    return license_evaluation_results


def apply_license_policy_to_component(
    component: License_Component,
    evaluation_results: dict,
    ignore_component_types: list,
) -> None:
    evaluation_result = None
    if component.purl_type in ignore_component_types:
        evaluation_result = License_Policy_Evaluation_Result.RESULT_IGNORED
    elif component.license:
        evaluation_result = evaluation_results.get(f"spdx_{component.license.spdx_id}")
    elif component.unknown_license:
        evaluation_result = evaluation_results.get(
            f"unknown_{component.unknown_license}"
        )
    if not evaluation_result:
        evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN

    component.evaluation_result = evaluation_result


def apply_license_policy(license_policy: License_Policy) -> None:
    products = Product.objects.filter(license_policy=license_policy)
    for product in products:
        license_evaluation_results = get_license_evaluation_results(product)
        components = License_Component.objects.filter(product=product)
        for component in components:
            license_before = component.license
            unknown_license_before = component.unknown_license
            evaluation_result_before = component.evaluation_result

            apply_license_policy_to_component(
                component,
                license_evaluation_results,
                get_ignore_component_type_list(license_policy.ignore_component_types),
            )

            if (
                license_before != component.license
                or unknown_license_before != component.unknown_license
                or evaluation_result_before != component.evaluation_result
            ):
                component.last_change = timezone.now()

            component.save()


def copy_license_policy(
    source_license_policy: License_Policy, name: str
) -> License_Policy:
    new_license_policy = License_Policy.objects.create(
        name=name,
        description=source_license_policy.description,
        is_public=source_license_policy.is_public,
        ignore_component_types=source_license_policy.ignore_component_types,
    )

    items = License_Policy_Item.objects.filter(license_policy=source_license_policy)
    for item in items:
        License_Policy_Item.objects.create(
            license_policy=new_license_policy,
            license_group=item.license_group,
            license=item.license,
            unknown_license=item.unknown_license,
            evaluation_result=item.evaluation_result,
        )

    members = License_Policy_Member.objects.filter(license_policy=source_license_policy)
    for member in members:
        License_Policy_Member.objects.update_or_create(
            license_policy=new_license_policy,
            user=member.user,
            is_manager=member.is_manager,
        )

    return new_license_policy


def get_ignore_component_type_list(ignore_component_types: str) -> list:
    ignore_component_types_list = (
        ignore_component_types.split(",") if ignore_component_types else []
    )
    ignore_component_types_list = [x.strip() for x in ignore_component_types_list]
    return ignore_component_types_list
