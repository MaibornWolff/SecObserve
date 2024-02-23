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
from application.vex.models import CSAF, Vulnerability, CSAF_Revision
from application.vex.services.vex_base import (
    check_either_product_or_vulnerability,
    get_and_check_product,
    get_observations_for_product,
    get_observations_for_vulnerability,
    get_vulnerability,
)


@dataclass(frozen=True)
class CSAFFullProductName:
    name: str
    product_id: str
    # product_identification_helper is still missing


@dataclass()
class CSAFProductTree:
    full_product_names: list[CSAFFullProductName]


@dataclass(frozen=True)
class CSAFNote:
    category: str
    text: str


@dataclass(frozen=True)
class CSAFFlag:
    label: str
    product_ids: list[str]


@dataclass(frozen=True)
class CSAFId:
    system_name: str
    text: str


@dataclass()
class CSAFProductStatus:
    fixed: list[str]
    known_affected: list[str]
    known_not_affected: list[str]
    under_investigation: list[str]


@dataclass()
class CSAFVulnerability:
    cve: str
    notes: list[CSAFNote]
    flags: list[CSAFFlag]
    ids: list[CSAFId]
    product_status: CSAFProductStatus
    # remediations are still missing


@dataclass()
class CSAFPublisher:
    name: str
    category: str
    namespace: str


@dataclass()
class CSAFEngine:
    name: str
    version: str


@dataclass()
class CSAFGenerator:
    engine: str


@dataclass(frozen=True)
class CSAFRevisionHistory:
    date: str
    number: str
    summary: str


@dataclass()
class CSAFTracking:
    id: str
    initial_release_date: str
    current_release_date: str
    version: str
    status: str
    generator: CSAFGenerator
    revision_history: list[CSAFRevisionHistory]


@dataclass()
class CSAFDocument:
    category: str
    csaf_version: str
    title: str
    publisher: CSAFPublisher
    tracking: CSAFTracking


@dataclass()
class CSAFRoot:
    document: CSAFDocument
    product_tree: CSAFProductTree
    vulnerabilities: list[CSAFVulnerability]

    def get_base_id(self) -> str:
        if len(self.document.tracking.id) > 36:
            return self.document.tracking.id[-36:]
        return ""


@dataclass()
class CSAFCreateParameters:
    product_id: int
    vulnerability_name: str
    document_id_prefix: str
    title: str
    publisher_name: str
    publisher_category: str
    publisher_namespace: str
    tracking_status: str


def create_csaf_document(parameters: CSAFCreateParameters) -> Optional[CSAFRoot]:
    check_either_product_or_vulnerability(
        parameters.product_id, parameters.vulnerability_name
    )

    product = get_and_check_product(parameters.product_id)
    vulnerability = get_vulnerability(parameters.vulnerability_name)
    document_base_id = str(uuid.uuid4())
    document_id = _get_document_id(parameters.document_id_prefix, document_base_id)

    _check_csaf_document_does_not_exist(product)

    if parameters.vulnerability_name is None:
        parameters.vulnerability_name = ""

    csaf = CSAF.objects.create(
        product=product,
        vulnerability_name=parameters.vulnerability_name,
        document_base_id=document_base_id,
        document_id=document_id,
        version=1,
        title=parameters.title,
        publisher_name=parameters.publisher_name,
        publisher_category=parameters.publisher_category,
        publisher_namespace=parameters.publisher_namespace,
        tracking_status=parameters.tracking_status,
    )
    CSAF_Revision.objects.create(
        csaf=csaf,
        revision_date=csaf.tracking_current_release_date,
        revision_version=1,
        summary="Initial release",
    )

    csaf_publisher = CSAFPublisher(
        name=csaf.publisher_name,
        category=csaf.publisher_category,
        namespace=csaf.publisher_namespace,
    )

    csaf_engine = CSAFEngine(
        name="SecOberserve",
        version=__version__,
    )

    csaf_generator = CSAFGenerator(
        engine=csaf_engine,
    )

    csaf_revision_history = CSAFRevisionHistory(
        date=csaf.tracking_initial_release_date.isoformat(),
        number=str(csaf.version),
        summary="Initial release",
    )

    csaf_tracking = CSAFTracking(
        id=csaf.document_id,
        initial_release_date=csaf.tracking_initial_release_date.isoformat(),
        current_release_date=csaf.tracking_current_release_date.isoformat(),
        version=str(csaf.version),
        status=csaf.tracking_status,
        generator=csaf_generator,
        revision_history=[csaf_revision_history],
    )

    csaf_document = CSAFDocument(
        category="csaf_vex",
        csaf_version="2.0",
        title=csaf.title,
        publisher=csaf_publisher,
        tracking=csaf_tracking,
    )

    csaf_root = CSAFRoot(
        document=csaf_document,
        product_tree=None,
        vulnerabilities=[],
    )

    return csaf_root


def _get_document_id(document_id_prefix: Optional[str], document_base_id: str) -> str:
    if not document_id_prefix:
        return document_base_id

    return document_id_prefix + "_" + document_base_id


def _check_csaf_document_does_not_exist(product: Optional[Product]):
    if product:
        try:
            CSAF.objects.get(product=product)
            raise ValidationError(
                f"CSAF document for product {product.id} already exists"
            )
        except CSAF.DoesNotExist:
            pass
