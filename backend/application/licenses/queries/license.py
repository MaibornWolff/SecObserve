from typing import Optional

from application.licenses.models import License


def get_license_by_license_id(license_id: str) -> Optional[License]:
    try:
        return License.objects.get(license_id=license_id)
    except License.DoesNotExist:
        return None
