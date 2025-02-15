from datetime import date, timedelta
from typing import Optional

from application.commons.models import Settings
from application.core.models import Product


def calculate_risk_acceptance_expiry_date(product: Product) -> Optional[date]:
    if product.risk_acceptance_expiry_active is False:
        return None
    if (
        product.risk_acceptance_expiry_active
        and product.risk_acceptance_expiry_days
        and product.risk_acceptance_expiry_days > 0
    ):
        return date.today() + timedelta(days=product.risk_acceptance_expiry_days)

    if product.product_group:
        if product.product_group.risk_acceptance_expiry_active is False:
            return None
        if (
            product.product_group.risk_acceptance_expiry_active
            and product.product_group.risk_acceptance_expiry_days
            and product.product_group.risk_acceptance_expiry_days > 0
        ):
            return date.today() + timedelta(days=product.product_group.risk_acceptance_expiry_days)

    settings = Settings.load()
    if settings.risk_acceptance_expiry_days > 0:
        return date.today() + timedelta(days=settings.risk_acceptance_expiry_days)

    return None
