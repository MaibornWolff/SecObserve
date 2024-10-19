from packageurl import PackageURL

from application.import_observations.models import Vulnerability_Check
from application.licenses.models import Component, Component_License
from application.licenses.queries.license import get_license_by_spdx_id
from application.licenses.services.license_policies import get_license_evaluation_result
from application.licenses.types import License_Policy_Evaluation_Result


def process_components(
    components: list[Component],
    vulnerability_check: Vulnerability_Check,
) -> None:
    existing_components = Component.objects.filter(
        component_license__vulnerability_check=vulnerability_check
    )
    existing_components_dict = {}
    for existing_component in existing_components:
        existing_components_dict[existing_component.name_version] = existing_component

    Component_License.objects.filter(vulnerability_check=vulnerability_check).delete()

    license_evaluation_results = get_license_evaluation_result(
        vulnerability_check.product
    )
    component_licenses: dict[str, Component_License] = {}

    for component in components:
        _prepare_component(component)
        existing_component: Component = existing_components_dict.get(
            component.name_version
        )
        if existing_component:
            existing_component.name = component.name
            existing_component.version = component.version
            existing_component.purl = component.purl
            existing_component.purl_type = component.purl_type
            existing_component.cpe = component.cpe
            existing_component.dependencies = component.dependencies
            existing_component.unsaved_license = component.unsaved_license
            _apply_license_policy(
                existing_component,
                vulnerability_check,
                component_licenses,
                license_evaluation_results,
            )
            existing_component.save()
            existing_components_dict.pop(component.name_version)
        else:
            _apply_license_policy(
                component,
                vulnerability_check,
                component_licenses,
                license_evaluation_results,
            )
            component.save()

    for existing_component in existing_components_dict.values():
        existing_component.delete()


def _prepare_component(component: Component) -> None:
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
            component.version = None

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


def _apply_license_policy(
    component: Component,
    vulnerability_check: Vulnerability_Check,
    component_licenses: dict[str, Component_License],
    evaluation_results: dict,
) -> None:
    if not component.unsaved_license:
        component_license = component_licenses.get("|no_license|")
        if not component_license:
            component_license = Component_License(
                vulnerability_check=vulnerability_check,
                license=None,
                unknown_license="",
                evaluation_result=License_Policy_Evaluation_Result.RESULT_UNKNOWN,
            )
            component_license.save()
            component_licenses["|no_license|"] = component_license
        component.component_license = component_license
        return

    unsaved_license = None
    unsaved_unknown_license = ""
    unsaved_license = get_license_by_spdx_id(component.unsaved_license)
    if unsaved_license:
        license_string = f"spdx_{unsaved_license.spdx_id}"
    else:
        unsaved_unknown_license = component.unsaved_license
        license_string = f"unknown_{unsaved_unknown_license}"

    unsaved_evaluation_result = License_Policy_Evaluation_Result.RESULT_UNKNOWN
    license_evaluation_result = None
    if unsaved_license:
        license_evaluation_result = evaluation_results.get(
            f"spdx_{unsaved_license.spdx_id}"
        )
    elif unsaved_unknown_license:
        license_evaluation_result = evaluation_results.get(
            f"unknown_{unsaved_unknown_license}"
        )
    if license_evaluation_result:
        unsaved_evaluation_result = license_evaluation_result

    component_license = component_licenses.get(license_string)
    if not component_license:
        component_license = Component_License(
            vulnerability_check=vulnerability_check,
            license=unsaved_license,
            unknown_license=unsaved_unknown_license,
            evaluation_result=unsaved_evaluation_result,
        )
        component_license.save()
        component_licenses[license_string] = component_license
    component.component_license = component_license
