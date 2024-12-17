import json
from dataclasses import dataclass
from typing import Optional

import yaml

from application.commons.services.export import object_to_json
from application.licenses.models import License_Policy, License_Policy_Item
from application.licenses.services.license_policy import get_ignore_component_type_list


@dataclass
class License_Policy_Export_Item:
    evaluation_result: str
    spdx_license: Optional[str] = None
    license_expression: Optional[str] = None
    unknown_license: Optional[str] = None
    license_group: Optional[str] = None


@dataclass
class License_Policy_Export_Ignore_Component_Type:
    component_type: str


@dataclass
class License_Policy_Export:
    name: str
    description: str
    items: list[License_Policy_Export_Item]
    ignore_component_types: list[License_Policy_Export_Ignore_Component_Type]


def export_license_policy_yaml(license_policy: License_Policy) -> str:
    return yaml.dump(json.loads(export_license_policy_json(license_policy)))


def export_license_policy_json(license_policy: License_Policy) -> str:
    return object_to_json(_create_license_policy_export(license_policy))


def _create_license_policy_export(
    license_policy: License_Policy,
) -> License_Policy_Export:
    license_policy_eport = License_Policy_Export(
        name=license_policy.name,
        description=license_policy.description,
        items=[],
        ignore_component_types=get_ignore_component_type_list(
            license_policy.ignore_component_types
        ),
    )

    license_policy_item: Optional[License_Policy_Item] = None
    for license_policy_item in license_policy.license_policy_items.all():
        if license_policy_item.license_group:
            for spdx_license in license_policy_item.license_group.licenses.all():
                license_policy_eport_item = License_Policy_Export_Item(
                    spdx_license=spdx_license.spdx_id,
                    license_group=license_policy_item.license_group.name,
                    evaluation_result=license_policy_item.evaluation_result,
                )
                license_policy_eport.items.append(license_policy_eport_item)
        elif license_policy_item.license:
            license_policy_eport_item = License_Policy_Export_Item(
                spdx_license=license_policy_item.license.spdx_id,
                evaluation_result=license_policy_item.evaluation_result,
            )
            license_policy_eport.items.append(license_policy_eport_item)
        elif license_policy_item.license_expression:
            license_policy_eport_item = License_Policy_Export_Item(
                license_expression=license_policy_item.license_expression,
                evaluation_result=license_policy_item.evaluation_result,
            )
            license_policy_eport.items.append(license_policy_eport_item)
        elif license_policy_item.unknown_license:
            license_policy_eport_item = License_Policy_Export_Item(
                unknown_license=license_policy_item.unknown_license,
                evaluation_result=license_policy_item.evaluation_result,
            )
            license_policy_eport.items.append(license_policy_eport_item)

    return license_policy_eport
