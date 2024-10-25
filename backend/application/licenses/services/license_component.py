import hashlib
from typing import Optional, Tuple

from django.db.models.query import QuerySet
from packageurl import PackageURL
from rest_framework.exceptions import ValidationError

from application.core.models import Product
from application.import_observations.models import Vulnerability_Check
from application.licenses.models import License_Component
from application.licenses.queries.license import get_license_by_spdx_id
from application.licenses.services.license_policy import (
    apply_license_policy_to_component,
    get_ignore_component_type_list,
    get_license_evaluation_results,
)


def get_identity_hash(observation) -> str:
    hash_string = _get_string_to_hash(observation)
    return hashlib.sha256(hash_string.casefold().encode("utf-8").strip()).hexdigest()


def _get_string_to_hash(
    license_component: License_Component,
):  # pylint: disable=too-many-branches
    hash_string = license_component.name_version
    if license_component.purl:
        hash_string += license_component.purl
    if license_component.dependencies:
        hash_string += license_component.dependencies
    if license_component.license:
        hash_string += license_component.license.spdx_id
    if license_component.unknown_license:
        hash_string += license_component.unknown_license

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

    license_evaluation_results = get_license_evaluation_results(
        vulnerability_check.product
    )

    components_new = 0
    components_updated = 0

    license_policy = vulnerability_check.product.license_policy
    ignore_component_types = (
        get_ignore_component_type_list(license_policy.ignore_component_types)
        if license_policy
        else []
    )

    for component in license_components:
        _prepare_component(component)
        existing_component = existing_components_dict.get(component.identity_hash)
        if existing_component:
            existing_component.name = component.name
            existing_component.version = component.version
            existing_component.purl = component.purl
            existing_component.purl_type = component.purl_type
            existing_component.cpe = component.cpe
            existing_component.dependencies = component.dependencies
            existing_component.license = component.license
            existing_component.unknown_license = component.unknown_license
            apply_license_policy_to_component(
                existing_component,
                license_evaluation_results,
                ignore_component_types,
            )
            existing_component.save()
            existing_components_dict.pop(component.identity_hash)
            components_updated += 1
        else:
            component.product = vulnerability_check.product
            component.branch = vulnerability_check.branch
            component.upload_filename = vulnerability_check.filename
            apply_license_policy_to_component(
                component,
                license_evaluation_results,
                ignore_component_types,
            )

            component.save()
            components_new += 1

    components_deleted = len(existing_components_dict)
    for existing_component in existing_components_dict.values():
        existing_component.delete()

    return components_new, components_updated, components_deleted


def _prepare_component(component: License_Component) -> None:
    _prepare_name_version(component)

    if component.name_version is None:
        component.name_version = ""
    if component.name is None:
        component.name = ""
    if component.version is None:
        component.version = ""
    if component.purl is None:
        component.purl = ""
    if component.cpe is None:
        component.cpe = ""
    if component.dependencies is None:
        component.dependencies = ""

    if component.purl:
        try:
            purl = PackageURL.from_string(component.purl)
            component.purl_type = purl.type
        except ValueError:
            component.purl_type = ""

    if component.purl_type is None:
        component.purl_type = ""

    if component.unsaved_license:
        component.license = get_license_by_spdx_id(component.unsaved_license)
        component.unknown_license = ""
        if not component.license:
            component.unknown_license = component.unsaved_license

    component.identity_hash = get_identity_hash(component)


def _prepare_name_version(component: License_Component) -> None:
    if not component.name_version:
        if component.name and component.version:
            component.name_version = component.name + ":" + component.version
        elif component.name:
            component.name_version = component.name
    else:
        component_parts = component.name_version.split(":")
        if len(component_parts) == 3:
            component.name = f"{component_parts[0]}:{component_parts[1]}"
            component.version = component_parts[2]
        elif len(component_parts) == 2:
            component.name = component_parts[0]
            component.version = component_parts[1]
        elif len(component_parts) == 1:
            component.name = component.name_version
            component.version = ""


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
