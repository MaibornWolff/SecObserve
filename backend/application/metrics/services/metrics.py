import logging
from datetime import date, timedelta
from typing import Optional

from constance import config
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons.services.tasks import handle_task_exception
from application.core.models import Observation, Product
from application.metrics.models import Product_Metrics
from application.metrics.queries.product_metrics import (
    get_product_metrics,
    get_todays_product_metrics,
)
from application.metrics.services.age import get_days

logger = logging.getLogger("secobserve.metrics")


@db_periodic_task(
    crontab(minute=f"*/{config.BACKGROUND_PRODUCT_METRICS_INTERVAL_MINUTES}")
)
@lock_task("calculate_product_metrics")
def calculate_product_metrics() -> None:
    logger.info("--- Calculate_product_metrics - start ---")

    try:
        for product in Product.objects.all():
            calculate_metrics_for_product(product)
    except Exception as e:
        handle_task_exception(e)

    logger.info("--- Calculate_product_metrics - finished ---")


def calculate_metrics_for_product(  # pylint: disable=too-many-branches
    product: Product,
) -> None:
    # There are quite a lot of branches, but at least they are not nested too much

    today = date.today()

    todays_product_metrics = Product_Metrics.objects.update_or_create(
        product=product,
        date=today,
        defaults={
            "open_critical": 0,
            "open_high": 0,
            "open_medium": 0,
            "open_low": 0,
            "open_none": 0,
            "open_unknown": 0,
            "open": 0,
            "resolved": 0,
            "duplicate": 0,
            "false_positive": 0,
            "in_review": 0,
            "not_affected": 0,
            "not_security": 0,
            "risk_accepted": 0,
        },
    )[0]

    observations = Observation.objects.filter(
        product=product,
        branch=product.repository_default_branch,
    ).values("current_severity", "current_status")

    for observation in observations:
        if observation.get("current_status") == Observation.STATUS_OPEN:
            todays_product_metrics.open += 1
            if observation.get("current_severity") == Observation.SEVERITY_CRITICAL:
                todays_product_metrics.open_critical += 1
            elif observation.get("current_severity") == Observation.SEVERITY_HIGH:
                todays_product_metrics.open_high += 1
            elif observation.get("current_severity") == Observation.SEVERITY_MEDIUM:
                todays_product_metrics.open_medium += 1
            elif observation.get("current_severity") == Observation.SEVERITY_LOW:
                todays_product_metrics.open_low += 1
            elif observation.get("current_severity") == Observation.SEVERITY_NONE:
                todays_product_metrics.open_none += 1
            elif observation.get("current_severity") == Observation.SEVERITY_UNKOWN:
                todays_product_metrics.open_unknown += 1
        elif observation.get("current_status") == Observation.STATUS_RESOLVED:
            todays_product_metrics.resolved += 1
        elif observation.get("current_status") == Observation.STATUS_DUPLICATE:
            todays_product_metrics.duplicate += 1
        elif observation.get("current_status") == Observation.STATUS_FALSE_POSITIVE:
            todays_product_metrics.false_positive += 1
        elif observation.get("current_status") == Observation.STATUS_IN_REVIEW:
            todays_product_metrics.in_review += 1
        elif observation.get("current_status") == Observation.STATUS_NOT_AFFECTED:
            todays_product_metrics.not_affected += 1
        elif observation.get("current_status") == Observation.STATUS_NOT_SECURITY:
            todays_product_metrics.not_security += 1
        elif observation.get("current_status") == Observation.STATUS_RISK_ACCEPTED:
            todays_product_metrics.risk_accepted += 1

    todays_product_metrics.save()


def get_severity_timeline(product: Optional[Product], age: str) -> dict:
    product_metrics = get_product_metrics()
    if product:
        product_metrics = product_metrics.filter(product=product)

    days = get_days(age)
    if days:
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_threshold = today - timedelta(days=int(days))
        product_metrics = product_metrics.filter(date__gte=time_threshold)

    response_data: dict = {}
    for product_metric in product_metrics:
        if not product:
            response_metric = response_data.get(product_metric.date.isoformat(), {})
            response_metric["open_critical"] = (
                response_metric.get("open_critical", 0) + product_metric.open_critical
            )
            response_metric["open_high"] = (
                response_metric.get("open_high", 0) + product_metric.open_high
            )
            response_metric["open_medium"] = (
                response_metric.get("open_medium", 0) + product_metric.open_medium
            )
            response_metric["open_low"] = (
                response_metric.get("open_low", 0) + product_metric.open_low
            )
            response_metric["open_none"] = (
                response_metric.get("open_none", 0) + product_metric.open_none
            )
            response_metric["open_unknown"] = (
                response_metric.get("open_unknown", 0) + product_metric.open_unknown
            )
            response_metric["open"] = (
                response_metric.get("open", 0) + product_metric.open
            )
            response_metric["resolved"] = (
                response_metric.get("resolved", 0) + product_metric.resolved
            )
            response_metric["duplicate"] = (
                response_metric.get("duplicate", 0) + product_metric.duplicate
            )
            response_metric["false_positive"] = (
                response_metric.get("false_positive", 0) + product_metric.false_positive
            )
            response_metric["in_review"] = (
                response_metric.get("in_review", 0) + product_metric.in_review
            )
            response_metric["not_affected"] = (
                response_metric.get("not_affected", 0) + product_metric.not_affected
            )
            response_metric["not_security"] = (
                response_metric.get("not_security", 0) + product_metric.not_security
            )
            response_metric["risk_accepted"] = (
                response_metric.get("risk_accepted", 0) + product_metric.risk_accepted
            )
            response_data[product_metric.date.isoformat()] = response_metric
        else:
            response_metric = {}
            response_metric["open_critical"] = product_metric.open_critical
            response_metric["open_high"] = product_metric.open_high
            response_metric["open_medium"] = product_metric.open_medium
            response_metric["open_low"] = product_metric.open_low
            response_metric["open_none"] = product_metric.open_none
            response_metric["open_unknown"] = product_metric.open_unknown
            response_metric["open"] = product_metric.open
            response_metric["resolved"] = product_metric.resolved
            response_metric["duplicate"] = product_metric.duplicate
            response_metric["false_positive"] = product_metric.false_positive
            response_metric["in_review"] = product_metric.in_review
            response_metric["not_affected"] = product_metric.not_affected
            response_metric["not_security"] = product_metric.not_security
            response_metric["risk_accepted"] = product_metric.risk_accepted
            response_data[product_metric.date.isoformat()] = response_metric
    return response_data


def get_severity_counts(product: Optional[Product]) -> dict:
    product_metrics = get_todays_product_metrics()
    if product:
        product_metrics = product_metrics.filter(product=product)

    response_data = {}
    response_data[Observation.SEVERITY_CRITICAL] = 0
    response_data[Observation.SEVERITY_HIGH] = 0
    response_data[Observation.SEVERITY_MEDIUM] = 0
    response_data[Observation.SEVERITY_LOW] = 0
    response_data[Observation.SEVERITY_NONE] = 0
    response_data[Observation.SEVERITY_UNKOWN] = 0

    for product_metric in product_metrics:
        response_data[Observation.SEVERITY_CRITICAL] += product_metric.open_critical
        response_data[Observation.SEVERITY_HIGH] += product_metric.open_high
        response_data[Observation.SEVERITY_MEDIUM] += product_metric.open_medium
        response_data[Observation.SEVERITY_LOW] += product_metric.open_low
        response_data[Observation.SEVERITY_NONE] += product_metric.open_none
        response_data[Observation.SEVERITY_UNKOWN] += product_metric.open_unknown

    return response_data


def get_status_counts(product: Optional[Product]) -> dict:
    product_metrics = get_todays_product_metrics()
    if product:
        product_metrics = product_metrics.filter(product=product)

    response_data = {}
    response_data[Observation.STATUS_OPEN] = 0
    response_data[Observation.STATUS_RESOLVED] = 0
    response_data[Observation.STATUS_DUPLICATE] = 0
    response_data[Observation.STATUS_FALSE_POSITIVE] = 0
    response_data[Observation.STATUS_IN_REVIEW] = 0
    response_data[Observation.STATUS_NOT_AFFECTED] = 0
    response_data[Observation.STATUS_NOT_SECURITY] = 0
    response_data[Observation.STATUS_RISK_ACCEPTED] = 0

    for product_metric in product_metrics:
        response_data[Observation.STATUS_OPEN] += product_metric.open
        response_data[Observation.STATUS_RESOLVED] += product_metric.resolved
        response_data[Observation.STATUS_DUPLICATE] += product_metric.duplicate
        response_data[
            Observation.STATUS_FALSE_POSITIVE
        ] += product_metric.false_positive
        response_data[Observation.STATUS_IN_REVIEW] += product_metric.in_review
        response_data[Observation.STATUS_NOT_AFFECTED] += product_metric.not_affected
        response_data[Observation.STATUS_NOT_SECURITY] += product_metric.not_security
        response_data[Observation.STATUS_RISK_ACCEPTED] += product_metric.risk_accepted

    return response_data


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
