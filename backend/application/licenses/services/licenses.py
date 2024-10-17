from json import loads

import requests

from application.licenses.models import License, License_Group
from application.licenses.queries.license import get_license_by_spdx_id


def import_licenses() -> None:
    response = requests.get(
        "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/licenses.json",
        timeout=60,
        stream=True,
    )
    response.raise_for_status()

    data = loads(response.content)
    licenses = data["licenses"]
    for spdx_license in licenses:
        spdx_id = spdx_license["licenseId"]
        try:
            secobserve_license = License.objects.get(spdx_id=spdx_id)
            license_changed = False
            if secobserve_license.name != spdx_license.get("name", ""):
                secobserve_license.name = spdx_license.get("name", "")
                license_changed = True
            if secobserve_license.reference != spdx_license.get("reference", ""):
                secobserve_license.reference = spdx_license.get("reference", "")
                license_changed = True
            if secobserve_license.is_osi_approved != spdx_license.get("isOsiApproved"):
                secobserve_license.is_osi_approved = spdx_license.get("isOsiApproved")
                license_changed = True
            if secobserve_license.is_deprecated != spdx_license.get(
                "isDeprecatedLicenseId"
            ):
                secobserve_license.is_deprecated = spdx_license.get(
                    "isDeprecatedLicenseId"
                )
                license_changed = True
            if license_changed:
                secobserve_license.save()
        except License.DoesNotExist:
            License.objects.create(
                spdx_id=spdx_id,
                name=spdx_license.get("name", ""),
                reference=spdx_license.get("reference", ""),
                is_osi_approved=spdx_license.get("isOsiApproved"),
                is_deprecated=spdx_license.get("isDeprecatedLicenseId"),
            )


def import_license_groups() -> None:
    if License_Group.objects.exists():
        return

    response = requests.get(
        "https://blueoakcouncil.org/list.json",
        timeout=60,
        stream=True,
    )
    response.raise_for_status()
    data = loads(response.content)
    _process_permissive_license_groups(data)

    response = requests.get(
        "https://blueoakcouncil.org/copyleft.json",
        timeout=60,
        stream=True,
    )
    response.raise_for_status()
    data = loads(response.content)
    _process_copyleft_license_groups(data)


def _process_permissive_license_groups(data: dict) -> None:
    ratings = data["ratings"]
    for rating in ratings:
        blue_oak_group_name = rating["name"]
        license_group = License_Group.objects.create(
            name=f"Permissive {blue_oak_group_name} (Blue Oak Council)",
            description=rating["notes"],
        )
        licenses = rating["licenses"]
        for blue_oak_license in licenses:
            spdx_id = blue_oak_license["id"]
            secobserve_license = get_license_by_spdx_id(spdx_id)
            if secobserve_license:
                license_group.licenses.add(secobserve_license)


def _process_copyleft_license_groups(data: dict) -> None:
    weak_license_group = License_Group.objects.create(
        name="Copyleft Weak (Blue Oak Council)",
        description="Weak copyleft licenses require sharing changes and additions "
        + "to the licensed software when you give copies to others.",
    )
    _process_copyleft_family(weak_license_group, data["families"]["weak"])

    strong_license_group = License_Group.objects.create(
        name="Copyleft Strong (Blue Oak Council)",
        description="In addition to the requirements of the weak copyleft licenses, strong copyleft licenses "
        + "require you to share larger programs that you build with the licensed software when you give copies "
        + "to others.",
    )
    _process_copyleft_family(strong_license_group, data["families"]["strong"])

    network_license_group = License_Group.objects.create(
        name="Copyleft Network (Blue Oak Council)",
        description="In addition to the requirements of strong copyleft licenses, network copyleft licenses "
        + "require you to share larger programs that you build with the licensed software not just when you "
        + "give copies to others, but also when you run the software for others to use over the Internet or "
        + "another network.",
    )
    _process_copyleft_family(network_license_group, data["families"]["network"])

    maximal_license_group = License_Group.objects.create(
        name="Copyleft Maximal (Blue Oak Council)",
        description="Maximal copyleft licenses answer the question “When does the license require you to share?” "
        + "differently than other families. Maximal copyleft licenses require you to share software you make with "
        + "others, and to license that software alike when you do.",
    )
    _process_copyleft_family(maximal_license_group, data["families"]["maximal"])


def _process_copyleft_family(license_group: License_Group, family: list) -> None:
    for name in family:
        for blue_oak_license in name["versions"]:
            spdx_id = blue_oak_license["id"]
            secobserve_license = get_license_by_spdx_id(spdx_id)
            if secobserve_license:
                license_group.licenses.add(secobserve_license)
