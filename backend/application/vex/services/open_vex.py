import hashlib
from dataclasses import dataclass
from typing import Optional

import jsonpickle
from rest_framework.exceptions import NotFound

from application.__init__ import __version__
from application.commons.services.global_request import get_current_user
from application.core.models import Branch, Observation, Observation_Log, Product
from application.core.types import Status
from application.vex.models import OpenVEX, OpenVEX_Branch, OpenVEX_Vulnerability
from application.vex.queries.open_vex import get_open_vex_by_document_id
from application.vex.services.open_vex_helpers import OpenVEXVulnerabilityCache
from application.vex.services.vex_base import (
    check_and_get_product,
    check_branch_names,
    check_product_or_vulnerabilities,
    check_vulnerability_names,
    create_document_base_id,
    get_component_id,
    get_observations_for_product,
    get_observations_for_vulnerability,
    get_product_id,
    get_vulnerability_url,
)
from application.vex.types import (
    OpenVEX_Status,
    OpenVEXDocument,
    OpenVEXProduct,
    OpenVEXProductIdentifiers,
    OpenVEXStatement,
    OpenVEXSubcomponent,
    OpenVEXVulnerability,
)


@dataclass()
class OpenVEXCreateParameters:
    product_id: int
    vulnerability_names: list[str]
    branch_names: list[str]
    id_namespace: str
    document_id_prefix: str
    author: str
    role: str


@dataclass()
class OpenVEXUpdateParameters:
    document_id_prefix: str
    document_base_id: str
    author: str
    role: str


def create_open_vex_document(
    parameters: OpenVEXCreateParameters,
) -> Optional[OpenVEXDocument]:
    check_product_or_vulnerabilities(
        parameters.product_id, parameters.vulnerability_names
    )

    product = check_and_get_product(parameters.product_id)
    check_vulnerability_names(parameters.vulnerability_names)
    branches = check_branch_names(parameters.branch_names, product)

    user = get_current_user()
    if not user:
        raise ValueError("No user in request")

    document_base_id = create_document_base_id(parameters.document_id_prefix)

    open_vex = OpenVEX.objects.create(
        product=product,
        id_namespace=parameters.id_namespace,
        document_id_prefix=parameters.document_id_prefix,
        document_base_id=document_base_id,
        author=parameters.author,
        role=parameters.role,
        version=1,
        user=user,
    )
    for vulnerability_name in parameters.vulnerability_names:
        if vulnerability_name is None:
            vulnerability_name = ""
        OpenVEX_Vulnerability.objects.create(openvex=open_vex, name=vulnerability_name)

    for branch in branches:
        OpenVEX_Branch.objects.create(openvex=open_vex, branch=branch)

    document_id = _get_document_id(
        parameters.id_namespace, parameters.document_id_prefix, document_base_id
    )
    open_vex_document = OpenVEXDocument(
        context="https://openvex.dev/ns/v0.2.0",
        id=document_id,
        version=open_vex.version,
        author=open_vex.author,
        role=open_vex.role,
        timestamp=open_vex.timestamp.isoformat(),
        last_updated=open_vex.last_updated.isoformat(),
        tooling="SecOberserve / " + __version__,
        statements=[],
    )

    statements = []
    if product:
        statements = _get_statements_for_product(
            product, parameters.vulnerability_names, branches
        )
    else:
        statements = _get_statements_for_vulnerabilities(parameters.vulnerability_names)

    if not statements:
        open_vex.delete()
        return None

    statements_json = jsonpickle.encode(statements, unpicklable=False)
    statements_hash = hashlib.sha256(
        statements_json.casefold().encode("utf-8").strip()
    ).hexdigest()
    open_vex.content_hash = statements_hash
    open_vex.save()

    for statement in statements:
        open_vex_document.statements.append(statement)

    return open_vex_document


def update_open_vex_document(
    parameters: OpenVEXUpdateParameters,
) -> Optional[OpenVEXDocument]:
    open_vex = get_open_vex_by_document_id(
        parameters.document_id_prefix, parameters.document_base_id
    )
    if not open_vex:
        raise NotFound(
            f"OpenVEX document with ids {parameters.document_id_prefix}"
            + f" and {parameters.document_base_id} does not exist"
        )

    open_vex_vulnerability_names = list(
        OpenVEX_Vulnerability.objects.filter(openvex=open_vex).values_list(
            "name", flat=True
        )
    )

    open_vex_branch_ids = OpenVEX_Branch.objects.filter(openvex=open_vex).values_list(
        "branch", flat=True
    )
    open_vex_branches = list(Branch.objects.filter(id__in=open_vex_branch_ids))

    statements = []
    if open_vex.product:
        statements = _get_statements_for_product(
            open_vex.product, open_vex_vulnerability_names, open_vex_branches
        )
    else:
        statements = _get_statements_for_vulnerabilities(open_vex_vulnerability_names)

    statements_json = jsonpickle.encode(statements, unpicklable=False)
    statements_hash = hashlib.sha256(
        statements_json.casefold().encode("utf-8").strip()
    ).hexdigest()

    if statements_hash == open_vex.content_hash:
        return None

    if parameters.author:
        open_vex.author = parameters.author
    if parameters.role:
        open_vex.role = parameters.role
    open_vex.version += 1
    open_vex.content_hash = statements_hash
    open_vex.save()

    document_id = _get_document_id(
        open_vex.id_namespace, open_vex.document_id_prefix, parameters.document_base_id
    )
    open_vex_document = OpenVEXDocument(
        context="https://openvex.dev/ns/v0.2.0",
        id=document_id,
        version=open_vex.version,
        author=open_vex.author,
        role=open_vex.role,
        timestamp=open_vex.timestamp.isoformat(),
        last_updated=open_vex.last_updated.isoformat(),
        tooling="SecOberserve / " + __version__,
        statements=[],
    )

    for statement in statements:
        open_vex_document.statements.append(statement)

    return open_vex_document


def _get_document_id(
    id_namespace: str, document_id_prefix: str, document_base_id: str
) -> str:
    if not id_namespace.endswith("/"):
        id_namespace += "/"

    return f"{id_namespace}{document_id_prefix}_{document_base_id}"


def _get_statements_for_vulnerabilities(
    vulnerability_names: list[str],
) -> list[OpenVEXStatement]:
    statements: dict[str, OpenVEXStatement] = {}

    for vulnerability_name in vulnerability_names:

        open_vex_vulnerability = OpenVEXVulnerability(
            name=vulnerability_name, id=get_vulnerability_url(vulnerability_name)
        )

        observations = get_observations_for_vulnerability(vulnerability_name)
        for observation in observations:
            prepared_statement = _prepare_statement(observation)
            if not prepared_statement:
                continue

            string_to_hash = (
                str(open_vex_vulnerability.name)
                + str(prepared_statement.status)
                + str(prepared_statement.justification)
                + str(prepared_statement.status_notes)
                + str(prepared_statement.action_statement)
            )
            hashed_string = hashlib.sha256(
                string_to_hash.casefold().encode("utf-8").strip()
            ).hexdigest()

            existing_statement = statements.get(hashed_string)
            if existing_statement:
                existing_product = get_open_vex_product_by_id(
                    existing_statement.products, get_product_id(observation)
                )
                if existing_product:
                    _add_subcomponent(observation, existing_product)
                else:
                    open_vex_product = _create_product(observation)
                    existing_statement.products.append(open_vex_product)
            else:
                if observation.description:
                    open_vex_vulnerability.description = observation.description
                prepared_statement.vulnerability = open_vex_vulnerability
                open_vex_product = _create_product(observation)
                prepared_statement.products.append(open_vex_product)
                statements[hashed_string] = prepared_statement

    return list(statements.values())


def _get_statements_for_product(
    product: Product, vulnerability_names: list[str], branches: list[Branch]
) -> list[OpenVEXStatement]:
    statements: dict[str, OpenVEXStatement] = {}

    vulnerability_cache = OpenVEXVulnerabilityCache()

    observations = get_observations_for_product(product, vulnerability_names, branches)
    for observation in observations:
        prepared_statement = _prepare_statement(observation)
        if not prepared_statement:
            continue

        open_vex_vulnerability = vulnerability_cache.get_vulnerability(
            observation.vulnerability_id
        )
        if not open_vex_vulnerability:
            open_vex_vulnerability = OpenVEXVulnerability(
                name=observation.vulnerability_id,
                description=observation.description,
                id=get_vulnerability_url(observation.vulnerability_id),
            )
            vulnerability_cache.add_vulnerability(open_vex_vulnerability)

        string_to_hash = (
            str(open_vex_vulnerability.name)
            + str(prepared_statement.status)
            + str(prepared_statement.justification)
            + str(prepared_statement.status_notes)
            + str(prepared_statement.action_statement)
            + str(prepared_statement.impact_statement)
        )
        hashed_string = hashlib.sha256(
            string_to_hash.casefold().encode("utf-8").strip()
        ).hexdigest()

        existing_statement = statements.get(hashed_string)
        if existing_statement:
            existing_product = get_open_vex_product_by_id(
                existing_statement.products, get_product_id(observation)
            )
            if existing_product:
                _add_subcomponent(observation, existing_product)
            else:
                raise ValueError(
                    f"Product {product.name} not found in existing statement"
                )
        else:
            prepared_statement.vulnerability = open_vex_vulnerability
            open_vex_product = _create_product(observation)
            prepared_statement.products.append(open_vex_product)
            statements[hashed_string] = prepared_statement

    return list(statements.values())


def _prepare_statement(observation: Observation) -> Optional[OpenVEXStatement]:
    open_vex_status = _map_status(observation.current_status)
    if not open_vex_status:
        return None

    open_vex_justification = None
    open_vex_impact_statement = None
    open_vex_action_statement = None
    open_vex_status_notes = None

    if open_vex_status == OpenVEX_Status.OPEN_VEX_STATUS_AFFECTED:
        if observation.recommendation:
            open_vex_action_statement = observation.recommendation
        else:
            open_vex_action_statement = (
                "No recommendation for remediation or mitigation available"
            )
    else:
        try:
            observation_log = Observation_Log.objects.filter(
                observation=observation
            ).latest("created")
        except Observation_Log.DoesNotExist:
            observation_log = None

        if open_vex_status == OpenVEX_Status.OPEN_VEX_STATUS_NOT_AFFECTED:
            if observation_log:
                if observation_log.vex_justification:
                    open_vex_justification = observation_log.vex_justification
                else:
                    open_vex_impact_statement = observation_log.comment
            else:
                open_vex_impact_statement = "No impact statement available"
        else:
            if observation_log:
                open_vex_status_notes = observation_log.comment

    return OpenVEXStatement(
        status=open_vex_status,
        status_notes=open_vex_status_notes,
        impact_statement=open_vex_impact_statement,
        justification=open_vex_justification,
        action_statement=open_vex_action_statement,
        vulnerability=None,
        products=[],
    )


def _map_status(secobserve_status: str) -> Optional[str]:
    if secobserve_status in (Status.STATUS_OPEN, Status.STATUS_RISK_ACCEPTED):
        return OpenVEX_Status.OPEN_VEX_STATUS_AFFECTED

    if secobserve_status == Status.STATUS_RESOLVED:
        return OpenVEX_Status.OPEN_VEX_STATUS_FIXED

    if secobserve_status in (
        Status.STATUS_NOT_AFFECTED,
        Status.STATUS_NOT_SECURITY,
        Status.STATUS_FALSE_POSITIVE,
    ):
        return OpenVEX_Status.OPEN_VEX_STATUS_NOT_AFFECTED

    if secobserve_status == Status.STATUS_IN_REVIEW:
        return OpenVEX_Status.OPEN_VEX_STATUS_UNDER_INVESTIGATION

    if secobserve_status == Status.STATUS_DUPLICATE:
        return None

    raise ValueError(f"Invalid status {secobserve_status}")


def get_open_vex_product_by_id(
    open_vex_products: list[OpenVEXProduct], product_id: str
) -> Optional[OpenVEXProduct]:
    for open_vex_product in open_vex_products:
        if open_vex_product.id == product_id:
            return open_vex_product
    return None


def _add_subcomponent(observation: Observation, existing_product: OpenVEXProduct):
    if get_component_id(observation):
        open_vex_subcomponent = OpenVEXSubcomponent(id=get_component_id(observation))
        if open_vex_subcomponent not in existing_product.subcomponents:
            existing_product.subcomponents.append(
                OpenVEXSubcomponent(id=get_component_id(observation))
            )


def _create_product(observation: Observation) -> OpenVEXProduct:
    open_vex_product_identifiers = None
    if observation.branch:
        if observation.branch.purl or observation.branch.cpe23:
            purl = observation.branch.purl if observation.branch.purl else None
            cpe23 = observation.branch.cpe23 if observation.branch.cpe23 else None
            open_vex_product_identifiers = OpenVEXProductIdentifiers(
                cpe23=cpe23, purl=purl
            )
    else:
        if observation.product.purl or observation.product.cpe23:
            purl = observation.product.purl if observation.product.purl else None
            cpe23 = observation.product.cpe23 if observation.product.cpe23 else None
            open_vex_product_identifiers = OpenVEXProductIdentifiers(
                cpe23=cpe23, purl=purl
            )

    open_vex_product = OpenVEXProduct(
        id=get_product_id(observation),
        subcomponents=[],
        identifiers=open_vex_product_identifiers,
    )

    _add_subcomponent(observation, open_vex_product)

    return open_vex_product
