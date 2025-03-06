from typing import Optional

from application.epss.models import Enriched_CVSS


def get_enriched_cvss_by_cve(cve: str) -> Optional[Enriched_CVSS]:
    try:
        return Enriched_CVSS.objects.get(cve=cve)
    except Enriched_CVSS.DoesNotExist:
        return None
