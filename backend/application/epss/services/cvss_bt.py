import datetime
from csv import DictReader
from io import StringIO

import requests
from cvss import CVSS3, CVSS4
from django.core.paginator import Paginator

from application.commons.models import Settings
from application.core.models import Observation
from application.core.services.observation import get_current_severity
from application.core.types import Status
from application.epss.models import Enriched_CVSS
from application.epss.queries.enriched_cvss import get_enriched_cvss_by_cve


def import_cvss_bt() -> None:
    response = requests.get(
        "https://raw.githubusercontent.com/t0sche/cvss-bt/refs/heads/main/cvss-bt.csv",
        timeout=5 * 60,
        stream=True,
    )
    response.raise_for_status()
    try:
        content = response.content.decode("utf-8")
        reader = DictReader(StringIO(content), delimiter=",", quotechar='"')
    except Exception:
        raise ValueError("File is not valid CSV")  # pylint: disable=raise-missing-from
        # The Exception itself is not relevant and must not be re-raised

    Enriched_CVSS.objects.all().delete()

    counter = 0
    enriched_cvss_s = []
    for row in reader:
        cve = row.get("cve", "")
        if not cve.startswith("CVE-"):
            continue
        cve_parts = cve.split("-")
        if len(cve_parts) != 3:
            continue
        cve_year = cve.split("-")[1]
        if not cve_year.isdigit():
            continue
        current_year = datetime.datetime.now().year
        settings = Settings.load()
        if int(cve_year) <= current_year - settings.cvss_enrichment_max_age_years:
            continue
        enriched_cvss_vector = row.get("cvss-bt_vector", "")
        if not enriched_cvss_vector.startswith("CVSS:3") and not enriched_cvss_vector.startswith("CVSS:4"):
            continue

        enriched_cvss = Enriched_CVSS(
            cve=cve,
            enriched_cvss_vector=enriched_cvss_vector,
            base_cvss_vector=row.get("base_vector", ""),
            cisa_kev=row.get("cisa_kev", "").lower() == "true",
            vulncheck_kev=row.get("vulncheck_kev", "").lower() == "true",
            exploitdb=row.get("exploitdb", "").lower() == "true",
            metasploit=row.get("metasploit", "").lower() == "true",
            nuclei=row.get("nuclei", "").lower() == "true",
            poc_github=row.get("poc_github", "").lower() == "true",
        )
        enriched_cvss_s.append(enriched_cvss)
        counter += 1
        if counter == 1000:
            Enriched_CVSS.objects.bulk_create(enriched_cvss_s)
            counter = 0
            enriched_cvss_s = []

    if enriched_cvss_s:
        Enriched_CVSS.objects.bulk_create(enriched_cvss_s)

    enriched_cvss_apply_observations(settings)


def enriched_cvss_apply_observations(settings: Settings) -> None:
    observations = (
        Observation.objects.filter(vulnerability_id__startswith="CVE-")
        .exclude(current_status=Status.STATUS_RESOLVED)
        .order_by("id")
    )

    paginator = Paginator(observations, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        updates = []

        for observation in page.object_list:
            if apply_enriched_cvss(observation, settings):
                updates.append(observation)

        Observation.objects.bulk_update(
            updates,
            [
                "cvss3_score",
                "cvss3_vector",
                "cvss4_score",
                "cvss4_vector",
                "enriched_cvss_score",
                "enriched_cvss_vector",
                "cve_found_in",
                "current_severity",
            ],
        )


def apply_enriched_cvss(observation: Observation, settings: Settings) -> bool:
    if not observation.vulnerability_id.startswith("CVE-"):
        return False

    if settings.feature_cvss_enrichment:  # pylint: disable=no-else-return
        # else shall stay for clarity and just in case a return would be forgotten
        enriched_cvss = get_enriched_cvss_by_cve(observation.vulnerability_id)
        if not enriched_cvss:
            return False

        if observation.cvss3_vector and not enriched_cvss.enriched_cvss_vector.startswith(observation.cvss3_vector):
            return False
        if observation.cvss4_vector and not enriched_cvss.enriched_cvss_vector.startswith(observation.cvss4_vector):
            return False

        observation.enriched_cvss_vector = enriched_cvss.enriched_cvss_vector
        if enriched_cvss.enriched_cvss_vector.startswith("CVSS:3"):
            cvss = CVSS3(observation.enriched_cvss_vector)
            observation.enriched_cvss_score = cvss.temporal_score
        else:
            cvss = CVSS4(observation.enriched_cvss_vector)
            observation.enriched_cvss_score = cvss.base_score

        if not observation.cvss3_vector and enriched_cvss.base_cvss_vector.startswith("CVSS:3"):
            observation.cvss3_vector = enriched_cvss.base_cvss_vector
            cvss = CVSS3(observation.cvss3_vector)
            observation.cvss3_score = cvss.temporal_score
        if not observation.cvss4_vector and enriched_cvss.base_cvss_vector.startswith("CVSS:4"):
            observation.cvss4_vector = enriched_cvss.base_cvss_vector
            cvss = CVSS4(observation.cvss4_vector)
            observation.cvss4_score = cvss.base_score

        _add_cve_found_in(observation, enriched_cvss)

        observation.current_severity = get_current_severity(observation)

        return True
    else:
        if observation.enriched_cvss_score or observation.enriched_cvss_vector or observation.cve_found_in:
            observation.enriched_cvss_score = None
            observation.enriched_cvss_vector = ""
            observation.cve_found_in = ""
            observation.current_severity = get_current_severity(observation)
            return True

        return False


def _add_cve_found_in(observation: Observation, enriched_cvss: Enriched_CVSS) -> None:
    cve_found_in = []
    if enriched_cvss.cisa_kev:
        cve_found_in.append("CISA KEV")
    if enriched_cvss.vulncheck_kev:
        cve_found_in.append("VulnCheck KEV")
    if enriched_cvss.exploitdb:
        cve_found_in.append("ExploitDB")
    if enriched_cvss.metasploit:
        cve_found_in.append("Metasploit")
    if enriched_cvss.nuclei:
        cve_found_in.append("Nuclei")
    if enriched_cvss.poc_github:
        cve_found_in.append("PoC GitHub")
    observation.cve_found_in = ", ".join(cve_found_in)
