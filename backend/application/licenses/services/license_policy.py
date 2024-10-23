from application.core.models import Product
from application.licenses.models import (
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)


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


def copy_license_policy(
    source_license_policy: License_Policy, name: str
) -> License_Policy:
    new_license_policy = License_Policy.objects.create(
        name=name,
        description=source_license_policy.description,
        is_public=source_license_policy.is_public,
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
