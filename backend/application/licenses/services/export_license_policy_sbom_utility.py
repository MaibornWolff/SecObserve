import json
from dataclasses import dataclass
from typing import Optional

import yaml

from application.commons.services.export import object_to_json
from application.licenses.models import License_Policy, License
from application.licenses.services.license_policy import (
    LicensePolicyEvaluationResult,
    get_license_evaluation_results_for_license_policy,
)
from application.licenses.types import License_Policy_Evaluation_Result

class USAGE_POLICY:
    POLICY_ALLOW = "allow"
    POLICY_DENY = "deny"
    POLICY_NEEDS_REVIEW = "needs-review"

@dataclass
class License_Policy_Export_Item:
    id: str
    name: str
    family: str
    reference: str
    osi: bool
    deprecated: bool
    usagePolicy: str
    annotationRefs: list[str]
    notes: str


@dataclass
class License_Policy_Export:
    policies: list[License_Policy_Export_Item]


def export_license_policy_sbom_utility(license_policy: License_Policy) -> str:
    return object_to_json(_create_license_policy_export(license_policy))


def _create_license_policy_export(
    license_policy: License_Policy,
) -> License_Policy_Export:
    license_policy_export = License_Policy_Export(policies=[])

    license_evaluation_results: dict[str, LicensePolicyEvaluationResult] = {}

    if license_policy.parent:
        get_license_evaluation_results_for_license_policy(license_policy.parent, True, license_evaluation_results)

    get_license_evaluation_results_for_license_policy(license_policy, False, license_evaluation_results)

    license_ids = set()
    for license_string in license_evaluation_results.keys():
        if license_string.startswith("spdx_"):
            license_ids.add(license_string.replace("spdx_", ""))

    spdx_licenses = License.objects.filter(spdx_id__in=license_ids)
    spdx_license_dict = {license.spdx_id: license for license in spdx_licenses}

    for license_string, evaluation_result in license_evaluation_results.items():
        license_id = license_string.replace("spdx_", "") if license_string.startswith("spdx_") else ""
        if license_id:
            license_name = spdx_license_dict.get(license_id, "").name
            reference = spdx_license_dict.get(license_id, "").reference
            osi = spdx_license_dict.get(license_id, "").is_osi_approved
            deprecated = spdx_license_dict.get(license_id, "").is_deprecated
        else:
            license_name = license_string.replace("expression_", "") if license_string.startswith("expression_") else ""
            if not license_name:
                license_name = license_string.replace("non_spdx_", "") if license_string.startswith("non_spdx_") else ""
            reference = ""
            osi = False
            deprecated = False

        family = license_id if license_id else license_name
        # replace everything that is not a letter, number or dash with a dash
        family = "".join(char if char.isalnum() or char == "-" else "-" for char in family)

        if evaluation_result.evaluation_result == License_Policy_Evaluation_Result.RESULT_ALLOWED:
            usagePolicy = USAGE_POLICY.POLICY_ALLOW
        elif evaluation_result.evaluation_result == License_Policy_Evaluation_Result.RESULT_FORBIDDEN:
            usagePolicy = USAGE_POLICY.POLICY_DENY
        elif evaluation_result.evaluation_result == License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED:
            usagePolicy = USAGE_POLICY.POLICY_NEEDS_REVIEW
        elif evaluation_result.evaluation_result == License_Policy_Evaluation_Result.RESULT_UNKNOWN:
            usagePolicy = USAGE_POLICY.POLICY_NEEDS_REVIEW
        elif evaluation_result.evaluation_result == License_Policy_Evaluation_Result.RESULT_IGNORED:
            usagePolicy = USAGE_POLICY.POLICY_ALLOW
        else:
            usagePolicy = USAGE_POLICY.POLICY_NEEDS_REVIEW
        annotationRefs = [evaluation_result.evaluation_result.upper()]

        license_policy_export_item = License_Policy_Export_Item(
            id=license_id,
            name=license_name,
            family=family,
            reference=reference,
            osi=osi,
            deprecated=deprecated,
            usagePolicy=usagePolicy,
            annotationRefs=annotationRefs,
            notes=[evaluation_result.comment],
        )

        license_policy_export.policies.append(license_policy_export_item)

    return license_policy_export
