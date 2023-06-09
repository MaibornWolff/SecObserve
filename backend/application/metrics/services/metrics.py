from django.db.models import Count

from application.core.models import Observation, Product
from application.core.queries.observation import get_observations


def get_severity_counts(product: Product = None):
    observations = get_observations()
    if product:
        observations = observations.filter(
            product=product, branch=product.repository_default_branch
        )

    return (
        observations.filter(current_status=Observation.STATUS_OPEN)
        .values("current_severity")
        .annotate(Count("id"))
    )


def get_status_counts(product: Product = None):
    observations = get_observations()
    if product:
        observations = observations.filter(
            product=product, branch=product.repository_default_branch
        )

    return observations.values("current_status").annotate(Count("id"))


def get_codecharta_metrics(product: Product) -> list[dict]:
    file_severities_dict: dict[str, dict] = {}
    observations = Observation.objects.filter(
        product=product, current_status=Observation.STATUS_OPEN
    )
    for observation in observations:
        if observation.origin_source_file:
            file_severities_value = file_severities_dict.get(
                observation.origin_source_file
            )
            if not file_severities_value:
                file_severities_value = {}
                file_severities_value["source_file"] = observation.origin_source_file
                file_severities_value["Vulnerabilities_Total".lower()] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_CRITICAL}".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_HIGH}".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_MEDIUM}".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_LOW}".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_NONE}".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_UNKOWN}".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_HIGH}_and_above".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_MEDIUM}_and_above".lower()
                ] = 0
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_LOW}_and_above".lower()
                ] = 0
                file_severities_dict[
                    observation.origin_source_file
                ] = file_severities_value

            file_severities_value["Vulnerabilities_Total".lower()] += 1
            file_severities_value[
                f"Vulnerabilities_{observation.current_severity}".lower()
            ] += 1

            if observation.current_severity in (
                Observation.SEVERITY_CRITICAL,
                Observation.SEVERITY_HIGH,
            ):
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_HIGH}_and_above".lower()
                ] += 1
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_MEDIUM}_and_above".lower()
                ] += 1
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_LOW}_and_above".lower()
                ] += 1

            if observation.current_severity == Observation.SEVERITY_MEDIUM:
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_MEDIUM}_and_above".lower()
                ] += 1
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_LOW}_and_above".lower()
                ] += 1

            if observation.current_severity == Observation.SEVERITY_LOW:
                file_severities_value[
                    f"Vulnerabilities_{Observation.SEVERITY_LOW}_and_above".lower()
                ] += 1

    return list(file_severities_dict.values())
