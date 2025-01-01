from typing import Optional

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.core.models import Branch, Observation, Product
from application.core.queries.observation import get_observations
from application.core.queries.product import get_product_by_id
from application.vex.models import VEX_Counter


def create_document_base_id(document_id_prefix: str) -> str:
    year = timezone.now().year
    counter = VEX_Counter.objects.get_or_create(
        document_id_prefix=document_id_prefix, year=year
    )[0]
    counter.counter += 1
    counter.save()
    return f"{counter.year}_{counter.counter:04d}"


def check_product_or_vulnerabilities(product_id, vulnerability_names):
    if not product_id and not vulnerability_names:
        raise ValidationError("Either product or vulnerabilities or both must be set")


def check_and_get_product(product_id: int) -> Optional[Product]:
    if not product_id:
        return None

    product = get_product_by_id(product_id, is_product_group=False)
    if not product:
        raise ValidationError(f"Product with id {product_id} does not exist")

    return product


def check_vulnerability_names(vulnerability_names: list[str]) -> None:
    if not vulnerability_names:
        return

    for vulnerability_name in vulnerability_names:
        if not Observation.objects.filter(vulnerability_id=vulnerability_name).exists():
            raise ValidationError(
                f"Vulnerability with name {vulnerability_name} does not exist"
            )


def check_branch_names(
    branch_names: list[str], product: Optional[Product]
) -> list[Branch]:
    if not branch_names:
        return []

    if not product:
        raise ValidationError("Product must be set when using branch_names")

    branches = Branch.objects.filter(name__in=branch_names, product=product)
    if len(branch_names) != len(branches):
        raise ValidationError("Some of the branch names do not exist")

    return list(branches)


def get_observations_for_vulnerability(
    vulnerability_name: str,
) -> list[Observation]:
    return list(
        get_observations().filter(vulnerability_id=vulnerability_name).order_by("id")
    )


def get_observations_for_product(
    product: Product, vulnerability_names: list[str], branches: list[Branch]
) -> list[Observation]:
    observations = (
        get_observations()
        .filter(product_id=product.pk)
        .exclude(vulnerability_id="")
        .order_by("id")
    )

    if vulnerability_names:
        observations = observations.filter(vulnerability_id__in=vulnerability_names)

    if branches:
        observations = observations.filter(branch__in=branches)

    return list(observations)


def get_product_id(observation: Observation) -> str:
    if observation.branch:
        if observation.branch.purl:
            return observation.branch.purl
        if observation.branch.cpe23:
            return observation.branch.cpe23
        return f"{observation.product.name}:{observation.branch.name}"

    if observation.product.purl:
        return observation.product.purl
    if observation.product.cpe23:
        return observation.product.cpe23
    return observation.product.name


def get_component_id(observation: Observation) -> str:
    if observation.origin_component_purl:
        return observation.origin_component_purl
    if observation.origin_component_cpe:
        return observation.origin_component_cpe
    return ""


VULNERABILITY_URLS = {
    "CVE": "https://nvd.nist.gov/vuln/detail/",
    "DLA": "https://security-tracker.debian.org/tracker/",
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
