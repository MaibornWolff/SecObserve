import hashlib
import uuid
from dataclasses import dataclass
from typing import Optional

import jsonpickle
import validators
from rest_framework.exceptions import ValidationError

from application.__init__ import __version__
from application.core.models import Observation, Observation_Log, Product
from application.core.types import Status
from application.vex.models import OpenVEX, Vulnerability
from application.vex.services.vex_base import (
    check_either_product_or_vulnerability,
    get_and_check_product,
    get_observations_for_product,
    get_observations_for_vulnerability,
    get_vulnerability,
)
from application.vex.types import OpenVEX_Status


@dataclass(frozen=True)
class OpenVEXProduct:
    id: str


@dataclass(frozen=True)
class OpenVEXVulnerability:
    name: str
    description: str


@dataclass
class OpenVEXStatement:
    status: str
    status_notes: Optional[str]
    justification: Optional[str]
    action_statement: Optional[str]
    vulnerability: Optional[OpenVEXVulnerability]
    products: list[OpenVEXProduct]


@dataclass
class OpenVEXDocument:
    context: str
    id: str
    version: int
    author: str
    role: str
    timestamp: str
    last_updated: str
    tooling: str
    statements: list[OpenVEXStatement]

    def get_base_id(self) -> str:
        if len(self.id) > 36:
            return self.id[-36:]
        return ""


def create_open_vex_document(
    product_id: int,
    vulnerability_name: str,
    document_id_prefix: str,
    author: str,
    role: str,
) -> Optional[OpenVEXDocument]:
    check_either_product_or_vulnerability(product_id, vulnerability_name)

    product = get_and_check_product(product_id)
    vulnerability = get_vulnerability(vulnerability_name)
    document_base_id = str(uuid.uuid4())
    document_id = _get_document_id(document_id_prefix, document_base_id)

    _check_open_vex_document_does_not_exist(product)

    if vulnerability_name is None:
        vulnerability_name = ""

    open_vex = OpenVEX.objects.create(
        product=product,
        vulnerability_name=vulnerability_name,
        document_base_id=document_base_id,
        document_id=document_id,
        author=author,
        role=role,
        version=1,
    )

    open_vex_document = OpenVEXDocument(
        context="https://openvex.dev/ns/v0.2.0",
        id=open_vex.document_id,
        version=open_vex.version,
        author=open_vex.author,
        role=open_vex.role,
        timestamp=open_vex.timestamp.isoformat(),
        last_updated=open_vex.last_updated.isoformat(),
        tooling="SecOberserve / " + __version__,
        statements=[],
    )

    statements = []
    if vulnerability and not product:
        statements = _get_statements_for_vulnerability(vulnerability)
    elif product and not vulnerability:
        statements = _get_statements_for_product(product)

    statements_json = jsonpickle.encode(statements, unpicklable=False)
    statements_hash = hashlib.sha256(
        statements_json.casefold().encode("utf-8").strip()
    ).hexdigest()
    open_vex.content_hash = statements_hash
    open_vex.save()

    if not statements:
        return None

    for statement in statements:
        open_vex_document.statements.append(statement)

    return open_vex_document


def update_open_vex_document(
    document_base_id: str, author: str, role: str
) -> Optional[OpenVEXDocument]:
    try:
        open_vex = OpenVEX.objects.get(document_base_id=document_base_id)
    except OpenVEX.DoesNotExist:
        raise ValidationError(  # pylint: disable=raise-missing-from
            f"OpenVEX document with id {document_base_id} does not exist"
        )
        # The DoesNotExist exception itself is not relevant and must not be re-raised

    statements = []
    if open_vex.vulnerability_name and not open_vex.product:
        vulnerability = get_vulnerability(open_vex.vulnerability_name)
        statements = _get_statements_for_vulnerability(vulnerability)
    elif open_vex.product and not open_vex.vulnerability_name:
        statements = _get_statements_for_product(open_vex.product)

    statements_json = jsonpickle.encode(statements, unpicklable=False)
    statements_hash = hashlib.sha256(
        statements_json.casefold().encode("utf-8").strip()
    ).hexdigest()

    if statements_hash == open_vex.content_hash:
        return None

    if author:
        open_vex.author = author
    if role:
        open_vex.role = role
    open_vex.version += 1
    open_vex.content_hash = statements_hash
    open_vex.save()

    open_vex_document = OpenVEXDocument(
        context="https://openvex.dev/ns/v0.2.0",
        id=open_vex.document_id,
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


def _check_open_vex_document_does_not_exist(product: Optional[Product]):
    if product:
        try:
            OpenVEX.objects.get(product=product)
            raise ValidationError(
                f"OpenVEX document for product {product.id} already exists"
            )
        except OpenVEX.DoesNotExist:
            pass


def _get_document_id(document_id_prefix: str, document_base_id: str) -> str:
    if not validators.url(document_id_prefix):
        raise ValidationError("Document ID prefix must be a valid URL")

    if not document_id_prefix.endswith("/"):
        document_id_prefix += "/"

    return document_id_prefix + "OpenVEX-" + document_base_id


def _get_statements_for_vulnerability(
    vulnerability: Vulnerability,
) -> list[OpenVEXStatement]:
    statements: dict[str, OpenVEXStatement] = {}

    open_vex_vulnerability = OpenVEXVulnerability(
        name=vulnerability.name, description=vulnerability.description
    )

    observations = get_observations_for_vulnerability(vulnerability)
    for observation in observations:
        prepared_statement = _prepare_statement(observation)
        if not prepared_statement:
            continue

        open_vex_product = OpenVEXProduct(id=observation.product.name)

        string_to_hash = (
            str(prepared_statement.status)
            + str(prepared_statement.justification)
            + str(prepared_statement.status_notes)
            + str(prepared_statement.action_statement)
        )
        hashed_string = hashlib.sha256(
            string_to_hash.casefold().encode("utf-8").strip()
        ).hexdigest()

        existing_statement = statements.get(hashed_string)
        if existing_statement:
            if open_vex_product not in existing_statement.products:
                existing_statement.products.append(open_vex_product)
        else:
            prepared_statement.vulnerability = open_vex_vulnerability
            prepared_statement.products.append(open_vex_product)
            statements[hashed_string] = prepared_statement

    return list(statements.values())


def _get_statements_for_product(product: Product) -> list[OpenVEXStatement]:
    statements: dict[str, OpenVEXStatement] = {}

    open_vex_product = OpenVEXProduct(id=product.name)

    observations = get_observations_for_product(product)
    for observation in observations:
        prepared_statement = _prepare_statement(observation)
        if not prepared_statement:
            continue

        open_vex_vulnerability = OpenVEXVulnerability(
            name=observation.vulnerability_id, description=observation.description
        )

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

        if not statements.get(hashed_string):
            prepared_statement.vulnerability = open_vex_vulnerability
            prepared_statement.products.append(open_vex_product)
            statements[hashed_string] = prepared_statement

    return list(statements.values())


def _prepare_statement(observation: Observation) -> Optional[OpenVEXStatement]:
    open_vex_status = _map_status(observation.current_status)
    if not open_vex_status:
        return None

    open_vex_justification = None

    open_vex_status_notes = None
    if open_vex_status != OpenVEX_Status.OPEN_VEX_STATUS_AFFECTED:
        try:
            observation_log = Observation_Log.objects.filter(
                observation=observation
            ).latest("created")
        except Observation_Log.DoesNotExist:
            observation_log = None
        if observation_log:
            open_vex_status_notes = observation_log.comment

    open_vex_action_statement = None
    if observation.recommendation:
        open_vex_action_statement = observation.recommendation

    return OpenVEXStatement(
        status=open_vex_status,
        status_notes=open_vex_status_notes,
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
