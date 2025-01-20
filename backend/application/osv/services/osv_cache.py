from datetime import datetime
from json import loads

import requests

from application.osv.models import OSV_Cache


def get_osv_vulnerability(osv_id: str, modified: datetime) -> dict:
    osv_vulnerability = OSV_Cache.objects.filter(osv_id=osv_id).first()
    if osv_vulnerability is None or osv_vulnerability.modified < modified:
        response = requests.get(
            url=f"https://api.osv.dev/v1/vulns/{osv_id}",
            timeout=60,
        )
        response.raise_for_status()
        osv_vulnerability, _ = OSV_Cache.objects.update_or_create(
            osv_id=osv_id, defaults={"modified": modified, "data": response.text}
        )

    return loads(osv_vulnerability.data)
