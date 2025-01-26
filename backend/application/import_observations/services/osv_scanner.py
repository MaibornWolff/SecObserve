from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

import jsonpickle
import requests

from application.core.models import Branch, Product
from application.import_observations.models import Vulnerability_Check
from application.import_observations.parsers.osv.parser import OSVParser
from application.import_observations.queries.parser import get_parser_by_name
from application.import_observations.services.import_observations import (
    ImportParameters,
    _process_data,
)
from application.import_observations.types import OSV_Component, OSV_Vulnerability
from application.licenses.models import License_Component


@dataclass
class Request_PURL:
    purl: str


@dataclass
class Request_Package:
    package: Request_PURL


@dataclass
class Request_Queries:
    queries: list[Request_Package]


def scan_product(product: Product) -> Tuple[int, int, int]:
    numbers: Tuple[int, int, int] = (0, 0, 0)

    branches = Branch.objects.filter(product=product)
    for branch in branches:
        (new, updated, resolved) = scan_branch(branch)
        numbers = (
            numbers[0] + new,
            numbers[1] + updated,
            numbers[2] + resolved,
        )

    license_components = get_license_components_no_branch(product)
    new, updated, resolved = scan_license_components(license_components, product, None)
    numbers = (
        numbers[0] + new,
        numbers[1] + updated,
        numbers[2] + resolved,
    )

    return numbers


def scan_branch(branch: Branch) -> Tuple[int, int, int]:
    license_components = get_license_components_for_branch(branch)
    return scan_license_components(license_components, branch.product, branch)


def get_license_components_for_branch(branch: Branch) -> list[License_Component]:
    return list(
        License_Component.objects.filter(branch=branch).exclude(component_purl="")
    )


def get_license_components_no_branch(product: Product) -> list[License_Component]:
    return list(
        License_Component.objects.filter(product=product, branch__isnull=True).exclude(
            component_purl=""
        )
    )


def scan_license_components(
    license_components: list[License_Component],
    product: Product,
    branch: Optional[Branch],
) -> Tuple[int, int, int]:
    if not license_components:
        return 0, 0, 0

    jsonpickle.set_encoder_options("json", ensure_ascii=False)

    queries = Request_Queries(
        queries=[
            Request_Package(Request_PURL(purl=license_component.component_purl))
            for license_component in license_components
        ]
    )

    response = requests.post(
        url="https://api.osv.dev/v1/querybatch",
        data=jsonpickle.encode(queries, unpicklable=False),
        timeout=5 * 60,
    )
    response.raise_for_status()
    results = response.json()

    osv_components = [
        OSV_Component(
            id=license_component.id,
            component_purl=license_component.component_purl,
            vulnerabilities=set(),
        )
        for license_component in license_components
    ]

    if len(osv_components) != len(results.get("results", [])):
        raise Exception(  # pylint: disable=broad-exception-raised
            "Number of results is different than number of components"
        )

    for result in results.get("results", []):
        if result.get("next_page_token"):
            raise Exception(  # pylint: disable=broad-exception-raised
                "Next page token is not yet supported"
            )

    for i, result in enumerate(results.get("results", [])):
        for vuln in result.get("vulns", []):
            osv_components[i].vulnerabilities.add(
                OSV_Vulnerability(
                    id=vuln.get("id"),
                    modified=datetime.fromisoformat(vuln.get("modified")),
                )
            )

    osv_parser = OSVParser()
    observations = osv_parser.get_observations(osv_components, product, branch)

    parser = get_parser_by_name(osv_parser.get_name())
    if parser is None:
        raise Exception(  # pylint: disable=broad-exception-raised
            f"Parser {osv_parser.get_name()} not found"
        )

    import_parameters = ImportParameters(
        product=license_components[0].product,
        branch=license_components[0].branch,
        parser=parser,
        filename="",
        api_configuration_name="",
        service="",
        docker_image_name_tag="",
        endpoint_url="",
        kubernetes_cluster="",
        imported_observations=observations,
    )
    numbers: Tuple[int, int, int, str] = _process_data(import_parameters)

    Vulnerability_Check.objects.update_or_create(
        product=import_parameters.product,
        branch=import_parameters.branch,
        filename="",
        api_configuration_name="",
        defaults={
            "last_import_observations_new": numbers[0],
            "last_import_observations_updated": numbers[1],
            "last_import_observations_resolved": numbers[2],
            "scanner": numbers[3],
        },
    )

    return numbers[0], numbers[1], numbers[2]
