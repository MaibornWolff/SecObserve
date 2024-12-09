from typing import Optional

from django.db.models import Q
from django.utils import timezone
from license_expression import LicenseSymbol, get_spdx_licensing

from application.core.models import Product
from application.licenses.models import (
    License_Component,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.queries.license import get_license_by_spdx_id
from application.licenses.types import License_Policy_Evaluation_Result


def get_license_evaluation_results(product: Product) -> dict:
    license_policy = _get_license_policy(product)
    if not license_policy:
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

    items_license_expressions = License_Policy_Item.objects.filter(
        license_policy=license_policy
    ).exclude(license_expression="")
    for item in items_license_expressions:
        license_evaluation_results[f"expression_{item.license_expression}"] = (
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
    elif component.license_expression:
        evaluation_result = _evaluate_license_expression(component, evaluation_results)
        if not evaluation_result:
            evaluation_result = evaluation_results.get(
                f"expression_{component.license_expression}"
            )
    elif component.unknown_license:
        evaluation_result = evaluation_results.get(
            f"unknown_{component.unknown_license}"
        )
    if not evaluation_result:
        evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN

    component.evaluation_result = evaluation_result


def apply_license_policy(license_policy: License_Policy) -> None:
    products = Product.objects.filter(
        Q(license_policy=license_policy)
        | (
            Q(product_group__license_policy=license_policy)
            & Q(license_policy__isnull=True)
        )
    )
    for product in products:
        apply_license_policy_product(product)


def apply_license_policy_product(product: Product) -> None:
    license_evaluation_results = get_license_evaluation_results(product)
    components = License_Component.objects.filter(product=product)
    for component in components:
        license_before = component.license
        unknown_license_before = component.unknown_license
        evaluation_result_before = component.evaluation_result

        license_policy = _get_license_policy(product)
        if license_policy:
            apply_license_policy_to_component(
                component,
                license_evaluation_results,
                get_ignore_component_type_list(license_policy.ignore_component_types),
            )
        else:
            component.evaluation_result = (
                License_Policy_Evaluation_Result.RESULT_UNKNOWN
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


def _get_license_policy(product: Product) -> Optional[License_Policy]:
    if product.license_policy:
        return product.license_policy

    if product.product_group and product.product_group.license_policy:
        return product.product_group.license_policy

    return None


def _evaluate_license_expression(
    component: License_Component, evaluation_results: dict
) -> Optional[str]:
    evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN

    try:
        licensing = get_spdx_licensing()
        parsed_expression = licensing.parse(
            component.license_expression, validate=True, strict=True
        )

        operator = parsed_expression.operator.strip().upper()
        if operator not in ["AND", "OR"]:
            return evaluation_result

        licenses = []
        for arg in parsed_expression.args:
            if isinstance(arg, LicenseSymbol):
                spdx_license = get_license_by_spdx_id(arg.key)
                if not spdx_license:
                    return evaluation_result
                licenses.append(spdx_license)
            else:
                return evaluation_results.get(
                    f"expression_{component.license_expression}"
                )

        evaluation_result_set = set()
        for spdx_license in licenses:
            if evaluation_results.get(f"spdx_{spdx_license.spdx_id}"):
                evaluation_result_set.add(
                    evaluation_results.get(f"spdx_{spdx_license.spdx_id}")
                )

        if operator == "AND":
            evaluation_result = _evaluate_and_expression(evaluation_result_set)

        if operator == "OR":
            evaluation_result = _evaluate_or_expression(evaluation_result_set)

    except Exception:  # nosec B110
        # a meaningful return value is set as a default in case on an exception
        pass

    return evaluation_result


def _evaluate_and_expression(evaluation_result_set: set) -> str:
    evaluation_result_set.discard(License_Policy_Evaluation_Result.RESULT_IGNORED)
    if not evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_UNKNOWN

    if License_Policy_Evaluation_Result.RESULT_FORBIDDEN in evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_FORBIDDEN
    if License_Policy_Evaluation_Result.RESULT_UNKNOWN in evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_UNKNOWN
    if License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED in evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED

    return License_Policy_Evaluation_Result.RESULT_ALLOWED


def _evaluate_or_expression(evaluation_result_set: set) -> str:
    evaluation_result_set.discard(License_Policy_Evaluation_Result.RESULT_IGNORED)
    if not evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_UNKNOWN

    if License_Policy_Evaluation_Result.RESULT_ALLOWED in evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_ALLOWED
    if License_Policy_Evaluation_Result.RESULT_UNKNOWN in evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_UNKNOWN
    if License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED in evaluation_result_set:
        return License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED

    return License_Policy_Evaluation_Result.RESULT_FORBIDDEN
