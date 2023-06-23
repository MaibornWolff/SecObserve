from constance import config

from application.commons.services.push_notifications import (
    send_product_security_gate_notification,
)
from application.core.models import Product


def check_security_gate(product: Product) -> None:
    initial_security_gate_passed = product.security_gate_passed
    new_security_gate_passed = None

    if product.security_gate_active is False:
        new_security_gate_passed = None
    elif product.security_gate_active is True:
        new_security_gate_passed = _calculate_active_product_security_gate(product)
    elif config.SECURITY_GATE_ACTIVE:
        new_security_gate_passed = _calculate_active_config_security_gate(product)

    if initial_security_gate_passed != new_security_gate_passed:
        product.security_gate_passed = new_security_gate_passed
        product.save()
        send_product_security_gate_notification(product)


def _calculate_active_product_security_gate(product: Product) -> bool:
    new_security_gate_passed = True

    if (
        product.open_critical_observation_count
        > product.security_gate_threshold_critical
    ):
        new_security_gate_passed = False
    elif product.open_high_observation_count > product.security_gate_threshold_high:
        new_security_gate_passed = False
    elif product.open_medium_observation_count > product.security_gate_threshold_medium:
        new_security_gate_passed = False
    elif product.open_low_observation_count > product.security_gate_threshold_low:
        new_security_gate_passed = False
    elif product.open_none_observation_count > product.security_gate_threshold_none:
        new_security_gate_passed = False
    elif product.open_unkown_observation_count > product.security_gate_threshold_unkown:
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
