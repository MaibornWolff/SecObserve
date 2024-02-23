from typing import Optional

from rest_framework.exceptions import ValidationError

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.models import Observation, Product
from application.core.queries.observation import get_observations
from application.core.queries.product import get_product_by_id


def check_either_product_or_vulnerabilities(product_id, vulnerability_names):
    if (product_id and vulnerability_names) or (
        not product_id and not vulnerability_names
    ):
        raise ValidationError("Either product or vulnerabilities must be set")


def check_and_get_product(product_id: int) -> Optional[Product]:
    if not product_id:
        return None

    product = get_product_by_id(product_id)
    if not product:
        raise ValidationError(f"Product with id {product_id} does not exist")

    user_has_permission_or_403(product, Permissions.Product_VEX)
    return product


def check_vulnerabilities(vulnerability_names: list[str]) -> None:
    if not vulnerability_names:
        return

    for vulnerability_name in vulnerability_names:
        if not Observation.objects.filter(vulnerability_id=vulnerability_name).exists():
            raise ValidationError(
                f"Vulnerability with name {vulnerability_name} does not exist"
            )


def get_observations_for_vulnerability(
    vulnerability_name: str,
) -> list[Observation]:
    observations = (
        get_observations().filter(vulnerability_id=vulnerability_name).order_by("id")
    )
    observations_list = []
    for observation in observations:
        if observation.branch == observation.product.repository_default_branch:
            observations_list.append(observation)
    return observations_list


def get_observations_for_product(
    product: Product,
) -> list[Observation]:
    return list(
        get_observations()
        .filter(product_id=product.pk, branch=product.repository_default_branch)
        .exclude(vulnerability_id="")
        .order_by("id")
    )


def get_product_id(product: Product) -> str:
    return product.name


def get_component_id(observation: Observation) -> str:
    if observation.origin_component_purl:
        return observation.origin_component_purl
    if observation.origin_component_cpe:
        return observation.origin_component_cpe
    return ""

VULNERABILITY_URLS = {
    "CVE": "https://nvd.nist.gov/vuln/detail/",
    "GHSA": "https://github.com/advisories/",
    "OSV": "https://osv.dev/vulnerability/",
    "PYSEC": "https://osv.dev/vulnerability/",
    "SNYK": "https://snyk.io/vuln/",
    "RUSTSEC": "https://rustsec.org/advisories/",
}


# create url for vulnerability
def get_vulnerability_url(vulnerability_name: str) -> Optional[str]:
    for key, value in VULNERABILITY_URLS.items():
        if vulnerability_name.startswith(key):
            return value + vulnerability_name
    return None
