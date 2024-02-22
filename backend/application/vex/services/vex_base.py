from typing import Optional

from rest_framework.exceptions import ValidationError

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.models import Observation, Product
from application.core.queries.observation import get_observations
from application.core.queries.product import get_product_by_id
from application.vex.models import Vulnerability


def check_either_product_or_vulnerability(product_id, vulnerability_name):
    if (product_id and vulnerability_name) or (
        not product_id and not vulnerability_name
    ):
        raise ValidationError("Either product or vulnerability must be set")


def get_and_check_product(product_id: int) -> Optional[Product]:
    if not product_id:
        return None

    product = get_product_by_id(product_id)
    if not product:
        raise ValidationError(f"Product with id {product_id} does not exist")

    user_has_permission_or_403(product, Permissions.Product_View)
    return product


def get_vulnerability(vulnerability_name: str) -> Optional[Vulnerability]:
    if not vulnerability_name:
        return None

    try:
        vulnerability = Vulnerability.objects.get(name=vulnerability_name)
    except Vulnerability.DoesNotExist:
        raise ValidationError(  # pylint: disable=raise-missing-from
            f"Vulnerability with name {vulnerability_name} does not exist"
        )
        # The DoesNotExist exception itself is not relevant and must not be re-raised

    return vulnerability


def get_observations_for_vulnerability(
    vulnerability: Vulnerability,
) -> list[Observation]:
    return list(
        get_observations().filter(vulnerability_id=vulnerability.name).order_by("id")
    )


def get_observations_for_product(
    product: Product,
) -> list[Observation]:
    return list(
        get_observations()
        .filter(product_id=product.id)
        .exclude(vulnerability_id="")
        .order_by("id")
    )
