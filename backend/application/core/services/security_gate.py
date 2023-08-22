from typing import Optional

from constance import config

from application.commons.services.send_notifications import (
    send_product_security_gate_notification,
)
from application.core.models import Product


def check_security_gate(product: Product) -> None:
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
    elif config.SECURITY_GATE_ACTIVE:
        new_security_gate_passed = _calculate_active_config_security_gate(product)

    if initial_security_gate_passed != new_security_gate_passed:
        product.security_gate_passed = new_security_gate_passed
        product.save()
        send_product_security_gate_notification(product)


def _calculate_active_product_security_gate(product: Product) -> bool:
    new_security_gate_passed = True

    if product.product_group and product.product_group.security_gate_active is True:
        security_gate_threshold_critical = (
            product.product_group.security_gate_threshold_critical
        )
        security_gate_threshold_high = (
            product.product_group.security_gate_threshold_high
        )
        security_gate_threshold_medium = (
            product.product_group.security_gate_threshold_medium
        )
        security_gate_threshold_low = product.product_group.security_gate_threshold_low
        security_gate_threshold_none = (
            product.product_group.security_gate_threshold_none
        )
        security_gate_threshold_unkown = (
            product.product_group.security_gate_threshold_unkown
        )
    else:
        security_gate_threshold_critical = product.security_gate_threshold_critical
        security_gate_threshold_high = product.security_gate_threshold_high
        security_gate_threshold_medium = product.security_gate_threshold_medium
        security_gate_threshold_low = product.security_gate_threshold_low
        security_gate_threshold_none = product.security_gate_threshold_none
        security_gate_threshold_unkown = product.security_gate_threshold_unkown

    if product.open_critical_observation_count > security_gate_threshold_critical:
        new_security_gate_passed = False
    elif product.open_high_observation_count > security_gate_threshold_high:
        new_security_gate_passed = False
    elif product.open_medium_observation_count > security_gate_threshold_medium:
        new_security_gate_passed = False
    elif product.open_low_observation_count > security_gate_threshold_low:
        new_security_gate_passed = False
    elif product.open_none_observation_count > security_gate_threshold_none:
        new_security_gate_passed = False
    elif product.open_unkown_observation_count > security_gate_threshold_unkown:
        new_security_gate_passed = False

    return new_security_gate_passed


def _calculate_active_config_security_gate(product: Product) -> bool:
    new_security_gate_passed = True

    if (
        product.open_critical_observation_count
        > config.SECURITY_GATE_THRESHOLD_CRITICAL
    ):
        new_security_gate_passed = False
    elif product.open_high_observation_count > config.SECURITY_GATE_THRESHOLD_HIGH:
        new_security_gate_passed = False
    elif product.open_medium_observation_count > config.SECURITY_GATE_THRESHOLD_MEDIUM:
        new_security_gate_passed = False
    elif product.open_low_observation_count > config.SECURITY_GATE_THRESHOLD_LOW:
        new_security_gate_passed = False
    elif product.open_none_observation_count > config.SECURITY_GATE_THRESHOLD_NONE:
        new_security_gate_passed = False
    elif product.open_unkown_observation_count > config.SECURITY_GATE_THRESHOLD_UNKOWN:
        new_security_gate_passed = False

    return new_security_gate_passed
