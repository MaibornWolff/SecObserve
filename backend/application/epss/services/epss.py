import gzip
import re
from datetime import datetime

import requests

from application.core.models import Observation
from application.epss.models import EPSS_Scores, EPSS_Status


def import_epss() -> None:
    response = requests.get(
        "https://epss.cyentia.com/epss_scores-current.csv.gz",
        timeout=60,
        stream=True,
    )
    response.raise_for_status()
    extracted_data = gzip.decompress(response.content)

    EPSS_Scores.objects.all().delete()

    counter = 0
    scores = []
    for line in extracted_data.split(b"\n"):
        decoded_line = line.decode()

        if decoded_line.startswith("#"):
            epss_date = re.search(r"(\d{4}-\d{2}-\d{2})", decoded_line)
            if epss_date:
                epss_status = EPSS_Status.load()
                epss_status.score_date = datetime.strptime(
                    epss_date.group(0), "%Y-%m-%d"
                )
                epss_status.save()

        if decoded_line.startswith("CVE"):
            elements = decoded_line.split(",")
            if len(elements) == 3:
                scores.append(
                    EPSS_Scores(
                        cve=elements[0],
                        epss_score=elements[1],
                        epss_percentile=elements[2],
                    )
                )
                counter += 1
            if counter == 1000:
                EPSS_Scores.objects.bulk_create(scores)
                counter = 0
                scores = []
    if scores:
        EPSS_Scores.objects.bulk_create(scores)


def epss_apply_observations() -> None:
    observations = Observation.objects.filter(title__startswith="CVE-")
    for observation in observations:
        epss_apply_observation(observation)


def epss_apply_observation(observation: Observation) -> None:
    if observation.title.startswith("CVE-"):
        try:
            epss_score = EPSS_Scores.objects.get(cve=observation.title)
        except EPSS_Scores.DoesNotExist:
            return

        if epss_score.epss_score:
            observation.epss_score = epss_score.epss_score * 100
        if epss_score.epss_percentile:
            observation.epss_percentile = epss_score.epss_percentile * 100
        observation.save()
