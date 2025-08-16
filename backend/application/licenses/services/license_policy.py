from dataclasses import dataclass
from typing import Optional

from django.db.models import Q
from django.utils import timezone
from license_expression import (
    AND,
    OR,
    LicenseExpression,
    LicenseSymbol,
    get_spdx_licensing,
)

from application.commons.services.functions import get_comma_separated_as_list
from application.core.models import Product
from application.licenses.models import (
    License,
    License_Component,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.queries.license import get_license_by_spdx_id
from application.licenses.types import License_Policy_Evaluation_Result


@dataclass
class LicensePolicyEvaluationResult:
    evaluation_result: str
    from_parent: bool
    license_group_name: Optional[str] = None
    comment: Optional[str] = None


def copy_license_policy(source_license_policy: License_Policy, name: str) -> License_Policy:
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
            non_spdx_license=item.non_spdx_license,
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


def get_license_evaluation_results_for_product(product: Product) -> dict:
    license_policy = get_license_policy(product)
    if not license_policy:
        return {}

    license_evaluation_results: dict[str, LicensePolicyEvaluationResult] = {}

    if license_policy.parent:
        get_license_evaluation_results_for_license_policy(license_policy.parent, True, license_evaluation_results)

    get_license_evaluation_results_for_license_policy(license_policy, False, license_evaluation_results)

    return license_evaluation_results


def get_license_evaluation_results_for_license_policy(
    license_policy: License_Policy,
    is_parent: bool,
    license_evaluation_results: dict[str, LicensePolicyEvaluationResult],
) -> None:
    items_license_groups = License_Policy_Item.objects.filter(
        license_policy=license_policy, license_group__isnull=False
    )
    for item in items_license_groups:
        if item.license_group:
            for my_license in item.license_group.licenses.all():
                license_evaluation_results[f"spdx_{my_license.spdx_id}"] = LicensePolicyEvaluationResult(
                    evaluation_result=item.evaluation_result,
                    from_parent=is_parent,
                    license_group_name=item.license_group.name,
                    comment=item.comment if item.comment else None,
                )

    items_licenses = License_Policy_Item.objects.filter(license_policy=license_policy, license__isnull=False)
    for item in items_licenses:
        if item.license:
            license_evaluation_results[f"spdx_{item.license.spdx_id}"] = LicensePolicyEvaluationResult(
                evaluation_result=item.evaluation_result,
                from_parent=is_parent,
                comment=item.comment if item.comment else None,
            )

    items_license_expressions = License_Policy_Item.objects.filter(license_policy=license_policy).exclude(
        license_expression=""
    )
    for item in items_license_expressions:
        license_evaluation_results[f"expression_{item.license_expression}"] = LicensePolicyEvaluationResult(
            evaluation_result=item.evaluation_result,
            from_parent=is_parent,
            comment=item.comment if item.comment else None,
        )

    items_non_spdx_licenses = License_Policy_Item.objects.filter(license_policy=license_policy).exclude(
        non_spdx_license=""
    )
    for item in items_non_spdx_licenses:
        license_evaluation_results[f"non_spdx_{item.non_spdx_license}"] = LicensePolicyEvaluationResult(
            evaluation_result=item.evaluation_result,
            from_parent=is_parent,
            comment=item.comment if item.comment else None,
        )


def apply_license_policy(license_policy: License_Policy) -> None:
    products = Product.objects.filter(
        Q(license_policy=license_policy)
        | (Q(product_group__license_policy=license_policy) & Q(license_policy__isnull=True))
    )
    for product in products:
        apply_license_policy_product(product)


def apply_license_policy_product(product: Product) -> None:
    license_evaluation_results = get_license_evaluation_results_for_product(product)
    components = License_Component.objects.filter(product=product)
    for component in components:
        evaluation_result_before = component.evaluation_result

        license_policy = get_license_policy(product)
        if license_policy:
            apply_license_policy_to_component(
                component,
                license_evaluation_results,
                get_comma_separated_as_list(license_policy.ignore_component_types),
            )
        else:
            component.evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN

        if evaluation_result_before != component.evaluation_result:
            component.last_change = timezone.now()

        component.save()


def apply_license_policy_to_component(
    component: License_Component,
    evaluation_results: dict[str, LicensePolicyEvaluationResult],
    ignore_component_types: list,
) -> None:
    evaluation_result = None
    if component.component_purl_type in ignore_component_types:
        evaluation_result = License_Policy_Evaluation_Result.RESULT_IGNORED
    elif component.effective_spdx_license:
        evaluation_result = _get_license_evaluation_result(
            f"spdx_{component.effective_spdx_license.spdx_id}", evaluation_results
        )
    elif component.effective_license_expression:
        evaluation_result = _evaluate_license_expression(component.effective_license_expression, evaluation_results)
    elif component.effective_non_spdx_license:
        evaluation_result = _get_license_evaluation_result(
            f"non_spdx_{component.effective_non_spdx_license}", evaluation_results
        )
    elif component.effective_multiple_licenses:
        evaluation_result = _get_multiple_licenses_evaluation_result(
            component.effective_multiple_licenses, evaluation_results
        )
    if not evaluation_result:
        evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN

    component.evaluation_result = evaluation_result


def get_license_policy(product: Product) -> Optional[License_Policy]:
    if product.license_policy:
        return product.license_policy

    if product.product_group and product.product_group.license_policy:
        return product.product_group.license_policy

    return None


def _get_license_evaluation_result(
    license_string: str, evaluation_results: dict[str, LicensePolicyEvaluationResult]
) -> str:
    evaluation_result = evaluation_results.get(license_string)
    if evaluation_result:
        return evaluation_result.evaluation_result

    return License_Policy_Evaluation_Result.RESULT_UNKNOWN


def _get_multiple_licenses_evaluation_result(
    multiple_licenses: str, evaluation_results: dict[str, LicensePolicyEvaluationResult]
) -> str:
    licenses = get_comma_separated_as_list(multiple_licenses)
    spdx_licenses = License.objects.filter(spdx_id__in=licenses).values_list("spdx_id", flat=True)

    evaluation_result_set = set()
    for license_string in licenses:
        if license_string in spdx_licenses:
            evaluation_result_set.add(_get_license_evaluation_result(f"spdx_{license_string}", evaluation_results))
        else:
            evaluation_result_set.add(_get_license_evaluation_result(f"non_spdx_{license_string}", evaluation_results))

    return _evaluate_and_expression(evaluation_result_set)


def _evaluate_license_expression(
    license_expression: str,
    evaluation_results: dict[str, LicensePolicyEvaluationResult],
) -> Optional[str]:
    evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN

    try:
        licensing = get_spdx_licensing()
        parsed_expression = licensing.parse(license_expression, validate=True, strict=True)
        evaluation_result = _evaluate_parsed_license_expression(parsed_expression, evaluation_results)
        if evaluation_result == License_Policy_Evaluation_Result.RESULT_UNKNOWN:
            evaluation_result = _get_license_evaluation_result(f"expression_{license_expression}", evaluation_results)
    except Exception:  # nosec B110
        # a meaningful return value is set as a default in case on an exception
        pass

    return evaluation_result


def _evaluate_parsed_license_expression(
    parsed_expression: LicenseExpression,
    evaluation_results: dict[str, LicensePolicyEvaluationResult],
) -> str:
    evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN

    parsed_expression_type = type(parsed_expression)
    if parsed_expression_type not in [AND, OR, LicenseSymbol]:
        return License_Policy_Evaluation_Result.RESULT_UNKNOWN

    if parsed_expression_type == LicenseSymbol:
        license_symbol = str(parsed_expression)
        spdx_license = get_license_by_spdx_id(license_symbol)
        if spdx_license:
            return _get_license_evaluation_result(f"spdx_{spdx_license.spdx_id}", evaluation_results)
        return License_Policy_Evaluation_Result.RESULT_UNKNOWN

    if parsed_expression_type in [AND, OR]:
        evaluation_result_set = set()
        for arg in parsed_expression.args:
            evaluation_result_set.add(_evaluate_parsed_license_expression(arg, evaluation_results))
        if parsed_expression_type == AND:
            evaluation_result = _evaluate_and_expression(evaluation_result_set)
        if parsed_expression_type == OR:
            evaluation_result = _evaluate_or_expression(evaluation_result_set)

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
