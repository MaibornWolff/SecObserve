from datetime import date, timedelta
from typing import Optional

from application.commons.models import Settings
from application.core.models import Product
from application.core.queries.branch import get_branches_by_product


def set_repository_default_branch(product: Product) -> None:
    if not product.repository_default_branch:
        current_repository_default_branch = product.repository_default_branch
        new_repository_default_branch = product.repository_default_branch
        branches = get_branches_by_product(product)
        if not branches:
            new_repository_default_branch = None
        else:
            if len(branches) == 1:
                new_repository_default_branch = branches[0]
            else:
                for branch in branches:
                    if branch.name == "main":
                        new_repository_default_branch = branch
                        break

        if new_repository_default_branch != current_repository_default_branch:
            product.repository_default_branch = new_repository_default_branch
            product.save()


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
            return date.today() + timedelta(
                days=product.product_group.risk_acceptance_expiry_days
            )

    settings = Settings.load()
    if settings.risk_acceptance_expiry_days > 0:
        return date.today() + timedelta(days=settings.risk_acceptance_expiry_days)

    return None
