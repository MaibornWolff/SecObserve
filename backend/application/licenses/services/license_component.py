import hashlib
from typing import Optional, Tuple

from django.db.models.query import QuerySet
from django.utils import timezone
from license_expression import get_spdx_licensing
from packageurl import PackageURL
from rest_framework.exceptions import ValidationError

from application.commons.services.functions import (
    clip_fields,
    get_comma_separated_as_list,
)
from application.core.models import Product
from application.import_observations.models import Vulnerability_Check
from application.licenses.models import License_Component, License_Component_Evidence
from application.licenses.queries.license import get_license_by_spdx_id
from application.licenses.services.license_policy import (
    apply_license_policy_to_component,
    get_license_evaluation_results_for_product,
)


def get_identity_hash(observation) -> str:
    hash_string = _get_string_to_hash(observation)
    return hashlib.sha256(hash_string.casefold().encode("utf-8").strip()).hexdigest()


def _get_string_to_hash(
    license_component: License_Component,
):  # pylint: disable=too-many-branches
    hash_string = license_component.component_name_version
    if license_component.component_purl:
        hash_string += license_component.component_purl
    if license_component.component_dependencies:
        hash_string += license_component.component_dependencies
    if license_component.license:
        hash_string += license_component.license.spdx_id
    if license_component.non_spdx_license:
        hash_string += license_component.non_spdx_license

    return hash_string


def process_license_components(
    license_components: list[License_Component],
    vulnerability_check: Vulnerability_Check,
) -> Tuple[int, int, int]:
    existing_components = License_Component.objects.filter(
        product=vulnerability_check.product,
        branch=vulnerability_check.branch,
        upload_filename=vulnerability_check.filename,
    )
    existing_component: Optional[License_Component] = None
    existing_components_dict: dict[str, License_Component] = {}
    for existing_component in existing_components:
        existing_components_dict[existing_component.identity_hash] = existing_component

    license_evaluation_results = get_license_evaluation_results_for_product(
        vulnerability_check.product
    )

    components_new = 0
    components_updated = 0

    license_policy = vulnerability_check.product.license_policy
    ignore_component_types = (
        get_comma_separated_as_list(license_policy.ignore_component_types)
        if license_policy
        else []
    )

    for unsaved_component in license_components:
        _prepare_component(unsaved_component)
        existing_component = existing_components_dict.get(
            unsaved_component.identity_hash
        )
        if existing_component:
            license_before = existing_component.license
            non_spdx_license_before = existing_component.non_spdx_license
            evaluation_result_before = existing_component.evaluation_result
            existing_component.component_name = unsaved_component.component_name
            existing_component.component_version = unsaved_component.component_version
            existing_component.component_purl = unsaved_component.component_purl
            existing_component.component_purl_type = (
                unsaved_component.component_purl_type
            )
            existing_component.component_cpe = unsaved_component.component_cpe
            existing_component.component_dependencies = (
                unsaved_component.component_dependencies
            )
            existing_component.license_name = unsaved_component.license_name
            existing_component.license = unsaved_component.license
            existing_component.license_expression = unsaved_component.license_expression
            existing_component.non_spdx_license = unsaved_component.non_spdx_license
            apply_license_policy_to_component(
                existing_component,
                license_evaluation_results,
                ignore_component_types,
            )
            existing_component.import_last_seen = timezone.now()
            if (
                license_before != existing_component.license
                or non_spdx_license_before != existing_component.non_spdx_license
                or evaluation_result_before != existing_component.evaluation_result
            ):
                existing_component.last_change = timezone.now()
            clip_fields("licenses", "License_Component", existing_component)
            existing_component.save()

            existing_component.evidences.all().delete()
            _process_evidences(unsaved_component, existing_component)

            existing_components_dict.pop(unsaved_component.identity_hash)
            components_updated += 1
        else:
            unsaved_component.product = vulnerability_check.product
            unsaved_component.branch = vulnerability_check.branch
            unsaved_component.upload_filename = vulnerability_check.filename
            apply_license_policy_to_component(
                unsaved_component,
                license_evaluation_results,
                ignore_component_types,
            )

            unsaved_component.import_last_seen = timezone.now()
            unsaved_component.last_change = timezone.now()
            clip_fields("licenses", "License_Component", unsaved_component)
            unsaved_component.save()

            _process_evidences(unsaved_component, unsaved_component)

            components_new += 1

    components_deleted = len(existing_components_dict)
    for existing_component in existing_components_dict.values():
        existing_component.delete()

    return components_new, components_updated, components_deleted


def _process_evidences(
    source_component: License_Component, target_component: License_Component
) -> None:
    if source_component.unsaved_evidences:
        for unsaved_evidence in source_component.unsaved_evidences:
            evidence = License_Component_Evidence(
                license_component=target_component,
                name=unsaved_evidence[0],
                evidence=unsaved_evidence[1],
            )
            clip_fields("licenses", "License_Component_Evidence", evidence)
            evidence.save()


def _prepare_component(component: License_Component) -> None:
    _prepare_name_version(component)

    if component.component_name_version is None:
        component.component_name_version = ""
    if component.component_name is None:
        component.component_name = ""
    if component.component_version is None:
        component.component_version = ""
    if component.component_purl is None:
        component.component_purl = ""
    if component.component_cpe is None:
        component.component_cpe = ""
    if component.component_dependencies is None:
        component.component_dependencies = ""

    if component.component_purl:
        try:
            purl = PackageURL.from_string(component.component_purl)
            component.component_purl_type = purl.type
        except ValueError:
            component.component_purl = ""
            component.component_purl_type = ""

    if component.component_purl_type is None:
        component.component_purl_type = ""

    _prepare_license(component)

    component.identity_hash = get_identity_hash(component)


def _prepare_name_version(component: License_Component) -> None:
    if not component.component_name_version:
        if component.component_name and component.component_version:
            component.component_name_version = (
                component.component_name + ":" + component.component_version
            )
        elif component.component_name:
            component.component_name_version = component.component_name
    else:
        component_parts = component.component_name_version.split(":")
        if len(component_parts) == 3:
            component.component_name = f"{component_parts[0]}:{component_parts[1]}"
            component.component_version = component_parts[2]
        elif len(component_parts) == 2:
            component.component_name = component_parts[0]
            component.component_version = component_parts[1]
        elif len(component_parts) == 1:
            component.component_name = component.component_name_version
            component.component_version = ""


def _prepare_license(component: License_Component) -> None:
    component.license_expression = ""
    component.non_spdx_license = ""

    component.license_name = component.unsaved_license

    if component.unsaved_license:
        component.license = get_license_by_spdx_id(component.unsaved_license)
        if not component.license:
            licensing = get_spdx_licensing()
            try:
                expression_info = licensing.validate(
                    component.unsaved_license, strict=True
                )
                if not expression_info.errors:
                    component.license_expression = expression_info.normalized_expression
                    component.license_name = component.license_expression
                else:
                    component.non_spdx_license = component.unsaved_license
            except Exception:
                component.non_spdx_license = component.unsaved_license

    if not component.license_name:
        component.license_name = "No license information"


def license_components_bulk_delete(product: Product, component_ids: list[int]) -> None:
    components = _check_components(product, component_ids)
    components.delete()


def _check_components(
    product: Product, component_ids: list[int]
) -> QuerySet[License_Component]:
    components = License_Component.objects.filter(id__in=component_ids)
    if len(components) != len(component_ids):
        raise ValidationError("Some components do not exist")

    for component in components:
        if component.product != product:
            raise ValidationError(
                f"Component {component.pk} does not belong to product {product.pk}"
            )

    return components
