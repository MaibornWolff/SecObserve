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
from application.vex.models import CSAF, CSAF_Revision
from application.vex.services.vex_base import (
    check_and_get_product,
    check_either_product_or_vulnerabilities,
    check_vulnerabilities,
    get_observations_for_product,
    get_observations_for_vulnerability,
)
from application.vex.types import (
    CSAFDocument,
    CSAFEngine,
    CSAFGenerator,
    CSAFPublisher,
    CSAFRevisionHistory,
    CSAFRoot,
    CSAFTracking,
)


@dataclass()
class CSAFCreateParameters:
    product_id: int
    vulnerability_names: list[str]
    document_id_prefix: str
    title: str
    publisher_name: str
    publisher_category: str
    publisher_namespace: str
    tracking_status: str


def create_csaf_document(parameters: CSAFCreateParameters) -> Optional[CSAFRoot]:
    check_either_product_or_vulnerabilities(
        parameters.product_id, parameters.vulnerability_name
    )
    product = check_and_get_product(parameters.product_id)
    check_vulnerabilities(parameters.vulnerability_names)
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

    csaf_root = _create_csaf_root(csaf)

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


def _create_csaf_root(csaf):
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
