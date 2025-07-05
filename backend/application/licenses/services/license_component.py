import hashlib

from django.db.models.query import QuerySet
from license_expression import get_spdx_licensing
from packageurl import PackageURL
from rest_framework.exceptions import ValidationError

from application.core.models import Product
from application.licenses.models import License_Component
from application.licenses.queries.license import get_license_by_spdx_id


def get_identity_hash(license_component: License_Component) -> str:
    hash_string = _get_string_to_hash(license_component)
    return hashlib.sha256(hash_string.casefold().encode("utf-8").strip()).hexdigest()


def _get_string_to_hash(
    license_component: License_Component,
) -> str:  # pylint: disable=too-many-branches
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


def prepare_license_component(component: License_Component) -> None:
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
            component.component_name_version = component.component_name + ":" + component.component_version
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
    component.multiple_licenses = ""

    component.license_name = component.unsaved_license
    if component.unsaved_license:
        if component.unsaved_license.startswith("[") and component.unsaved_license.endswith("]"):
            component.multiple_licenses = component.unsaved_license[1:-1]
            component.license_name = component.multiple_licenses
        if not component.multiple_licenses:
            component.license = get_license_by_spdx_id(component.unsaved_license)
        if not component.multiple_licenses and not component.license:
            licensing = get_spdx_licensing()
            try:
                expression_info = licensing.validate(component.unsaved_license, strict=True)
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


def _check_components(product: Product, component_ids: list[int]) -> QuerySet[License_Component]:
    components = License_Component.objects.filter(id__in=component_ids)
    if len(components) != len(component_ids):
        raise ValidationError("Some components do not exist")

    for component in components:
        if component.product != product:
            raise ValidationError(f"Component {component.pk} does not belong to product {product.pk}")

    return components
