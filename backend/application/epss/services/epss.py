import gzip
import re
from datetime import datetime

import requests
from django.core.paginator import Paginator

from application.core.models import Observation
from application.core.types import Status
from application.epss.models import EPSS_Score, EPSS_Status


def import_epss() -> None:
    response = requests.get(
        "https://epss.cyentia.com/epss_scores-current.csv.gz",
        timeout=60,
        stream=True,
    )
    response.raise_for_status()
    extracted_data = gzip.decompress(response.content)

    EPSS_Score.objects.all().delete()

    counter = 0
    scores = []
    for line in extracted_data.split(b"\n"):
        decoded_line = line.decode()

        if decoded_line.startswith("#"):
            epss_date = re.search(r"(\d{4}-\d{2}-\d{2})", decoded_line)
            if epss_date:
                epss_status = EPSS_Status.load()
                epss_status.score_date = datetime.strptime(epss_date.group(0), "%Y-%m-%d")
                epss_status.save()

        if decoded_line.startswith("CVE"):
            elements = decoded_line.split(",")
            if len(elements) == 3:
                scores.append(
                    EPSS_Score(
                        cve=elements[0],
                        epss_score=elements[1],
                        epss_percentile=elements[2],
                    )
                )
                counter += 1
            if counter == 1000:
                EPSS_Score.objects.bulk_create(scores)
                counter = 0
                scores = []
    if scores:
        EPSS_Score.objects.bulk_create(scores)


def epss_apply_observations() -> None:
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
            if apply_epss(observation):
                updates.append(observation)

        Observation.objects.bulk_update(updates, ["epss_score", "epss_percentile"])


def apply_epss(observation: Observation) -> bool:
    if observation.vulnerability_id.startswith("CVE-"):
        try:
            epss_score = EPSS_Score.objects.get(cve=observation.vulnerability_id)
        except EPSS_Score.DoesNotExist:
            return False

        new_epss_score = round(epss_score.epss_score * 100, 3) if epss_score.epss_score else None
        new_epss_percentile = round(epss_score.epss_percentile * 100, 3) if epss_score.epss_percentile else None
        if observation.epss_score != new_epss_score or observation.epss_percentile != new_epss_percentile:
            observation.epss_score = new_epss_score
            observation.epss_percentile = new_epss_percentile
            return True

    return False
