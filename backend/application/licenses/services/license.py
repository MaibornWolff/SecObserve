from json import loads

import requests

from application.licenses.models import License


def import_licenses() -> str:

    licenses_updated = 0
    licenses_created = 0

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
            if secobserve_license.is_deprecated != spdx_license.get("isDeprecatedLicenseId"):
                secobserve_license.is_deprecated = spdx_license.get("isDeprecatedLicenseId")
                license_changed = True
            if license_changed:
                secobserve_license.save()
                licenses_updated += 1
        except License.DoesNotExist:
            License.objects.create(
                spdx_id=spdx_id,
                name=spdx_license.get("name", ""),
                reference=spdx_license.get("reference", ""),
                is_osi_approved=spdx_license.get("isOsiApproved"),
                is_deprecated=spdx_license.get("isDeprecatedLicenseId"),
            )
            licenses_created += 1

    return f"Licenses updated: {licenses_updated}, licenses created: {licenses_created}"
