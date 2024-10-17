from packageurl import PackageURL

from application.import_observations.models import Vulnerability_Check
from application.licenses.models import Component
from application.licenses.queries.license import get_license_by_spdx_id


def process_components(
    components: list[Component], vulnerability_check: Vulnerability_Check
) -> None:
    existing_components = Component.objects.filter(
        vulnerability_check=vulnerability_check
    )
    existing_components_dict = {}
    for existing_component in existing_components:
        existing_components_dict[existing_component.name_version] = existing_component

    for component in components:
        prepare_component(component, vulnerability_check)
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
            existing_component.license = component.license
            existing_component.unknown_license = component.unknown_license
            existing_component.save()
            existing_components_dict.pop(component.name_version)
        else:
            component.save()

    for existing_component in existing_components_dict.values():
        existing_component.delete()


def prepare_component(
    component: Component, vulnerability_check: Vulnerability_Check
) -> None:
    component.vulnerability_check = vulnerability_check
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

    my_license = get_license_by_spdx_id(component.unknown_license)
    if my_license:
        component.license = my_license
        component.unknown_license = ""
