from typing import Optional

from application.commons.models import Settings
from application.core.models import Observation, Product
from application.core.services.product import get_product_observation_count
from application.core.types import Severity
from application.notifications.services.send_notifications import (
    send_product_security_gate_notification,
)


def check_security_gate(product: Product) -> None:
    if product.is_product_group:
        raise ValueError(f"{product.name} is a product group")

    settings = Settings.load()

    initial_security_gate_passed = product.security_gate_passed
    new_security_gate_passed = None

    security_gate_active: Optional[bool]
    if product.product_group and product.product_group.security_gate_active is not None:
        security_gate_active = product.product_group.security_gate_active
    else:
        security_gate_active = product.security_gate_active

    if security_gate_active is False:
        new_security_gate_passed = None
    elif security_gate_active is True:
        new_security_gate_passed = _calculate_active_product_security_gate(product)
    elif settings.security_gate_active:
        new_security_gate_passed = _calculate_active_config_security_gate(product)

    if initial_security_gate_passed != new_security_gate_passed:
        product.security_gate_passed = new_security_gate_passed
        product.save()
        send_product_security_gate_notification(product)


def check_security_gate_observation(observation: Observation) -> None:
    if observation.branch == observation.product.repository_default_branch:
        check_security_gate(observation.product)


def _calculate_active_product_security_gate(product: Product) -> bool:
    new_security_gate_passed = True

    if product.product_group and product.product_group.security_gate_active is True:
        security_gate_threshold_critical = (
            product.product_group.security_gate_threshold_critical
            if product.product_group.security_gate_threshold_critical
            else 0
        )
        security_gate_threshold_high = (
            product.product_group.security_gate_threshold_high
            if product.product_group.security_gate_threshold_high
            else 0
        )
        security_gate_threshold_medium = (
            product.product_group.security_gate_threshold_medium
            if product.product_group.security_gate_threshold_medium
            else 0
        )
        security_gate_threshold_low = (
            product.product_group.security_gate_threshold_low
            if product.product_group.security_gate_threshold_low
            else 0
        )
        security_gate_threshold_none = (
            product.product_group.security_gate_threshold_none
            if product.product_group.security_gate_threshold_none
            else 0
        )
        security_gate_threshold_unknown = (
            product.product_group.security_gate_threshold_unknown
            if product.product_group.security_gate_threshold_unknown
            else 0
        )
    else:
        security_gate_threshold_critical = (
            product.security_gate_threshold_critical if product.security_gate_threshold_critical else 0
        )
        security_gate_threshold_high = (
            product.security_gate_threshold_high if product.security_gate_threshold_high else 0
        )
        security_gate_threshold_medium = (
            product.security_gate_threshold_medium if product.security_gate_threshold_medium else 0
        )
        security_gate_threshold_low = product.security_gate_threshold_low if product.security_gate_threshold_low else 0
        security_gate_threshold_none = (
            product.security_gate_threshold_none if product.security_gate_threshold_none else 0
        )
        security_gate_threshold_unknown = (
            product.security_gate_threshold_unknown if product.security_gate_threshold_unknown else 0
        )

    if (
        get_product_observation_count(  # pylint: disable=too-many-boolean-expressions
            product, Severity.SEVERITY_CRITICAL
        )
        > security_gate_threshold_critical
        or get_product_observation_count(product, Severity.SEVERITY_HIGH) > security_gate_threshold_high
        or get_product_observation_count(product, Severity.SEVERITY_MEDIUM) > security_gate_threshold_medium
        or get_product_observation_count(product, Severity.SEVERITY_LOW) > security_gate_threshold_low
        or get_product_observation_count(product, Severity.SEVERITY_NONE) > security_gate_threshold_none
        or get_product_observation_count(product, Severity.SEVERITY_UNKNOWN) > security_gate_threshold_unknown
    ):
        new_security_gate_passed = False

    return new_security_gate_passed


def _calculate_active_config_security_gate(product: Product) -> bool:
    settings = Settings.load()

    new_security_gate_passed = True
    if (
        get_product_observation_count(  # pylint: disable=too-many-boolean-expressions
            product, Severity.SEVERITY_CRITICAL
        )
        > settings.security_gate_threshold_critical
        or get_product_observation_count(product, Severity.SEVERITY_HIGH) > settings.security_gate_threshold_high
        or get_product_observation_count(product, Severity.SEVERITY_MEDIUM) > settings.security_gate_threshold_medium
        or get_product_observation_count(product, Severity.SEVERITY_LOW) > settings.security_gate_threshold_low
        or get_product_observation_count(product, Severity.SEVERITY_NONE) > settings.security_gate_threshold_none
        or get_product_observation_count(product, Severity.SEVERITY_UNKNOWN) > settings.security_gate_threshold_unknown
    ):
        new_security_gate_passed = False

    return new_security_gate_passed
