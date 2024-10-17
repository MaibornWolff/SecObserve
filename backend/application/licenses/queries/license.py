from typing import Optional

from application.licenses.models import License


def get_license_by_spdx_id(spdx_id: str) -> Optional[License]:
    try:
        return License.objects.get(spdx_id=spdx_id)
    except License.DoesNotExist:
        return None
