import hashlib
import uuid
from dataclasses import dataclass
from typing import Optional

import jsonpickle
from rest_framework.exceptions import NotFound

from application.__init__ import __version__
from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Observation_Log, Product
from application.core.types import Status
from application.vex.models import CSAF, CSAF_Revision, CSAF_Vulnerability
from application.vex.services.csaf_helpers import get_vulnerability_ecosystem
from application.vex.services.vex_base import (
    check_and_get_product,
    check_product_or_vulnerabilities,
    check_vulnerabilities,
    get_observations_for_product,
    get_observations_for_vulnerability,
    get_vulnerability_url,
)
from application.vex.types import (
    CSAFTLP,
    CSAF_Status,
    CSAFDistribution,
    CSAFDocument,
    CSAFEngine,
    CSAFFullProductName,
    CSAFGenerator,
    CSAFId,
    CSAFNote,
    CSAFProductStatus,
    CSAFProductTree,
    CSAFPublisher,
    CSAFReference,
    CSAFRemediation,
    CSAFRevisionHistory,
    CSAFRoot,
    CSAFThreat,
    CSAFTracking,
    CSAFVulnerability,
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
    tlp_label: str


@dataclass()
class CSAFUpdateParameters:
    document_base_id: str
    publisher_name: str
    publisher_category: str
    publisher_namespace: str
    tracking_status: str


@dataclass()
class CSAFContent:
    vulnerabilities: list[CSAFVulnerability]
    product_tree: CSAFProductTree


def create_csaf_document(parameters: CSAFCreateParameters) -> Optional[CSAFRoot]:
    check_product_or_vulnerabilities(
        parameters.product_id, parameters.vulnerability_names
    )
    product = check_and_get_product(parameters.product_id)
    check_vulnerabilities(parameters.vulnerability_names)
    document_base_id = str(uuid.uuid4())

    user = get_current_user()
    if not user:
        raise ValueError("No user in request")

    csaf = CSAF.objects.create(
        product=product,
        document_id_prefix=parameters.document_id_prefix,
        document_base_id=document_base_id,
        document_id="to be done",
        version=1,
        title=parameters.title,
        publisher_name=parameters.publisher_name,
        publisher_category=parameters.publisher_category,
        publisher_namespace=parameters.publisher_namespace,
        tracking_status=parameters.tracking_status,
        tlp_label=parameters.tlp_label,
        user=user,
    )
    CSAF_Revision.objects.create(
        csaf=csaf,
        date=csaf.tracking_current_release_date,
        version=1,
        summary="Initial release",
    )
    for vulnerability_name in parameters.vulnerability_names:
        if vulnerability_name is None:
            vulnerability_name = ""
        CSAF_Vulnerability.objects.create(csaf=csaf, name=vulnerability_name)

    csaf_root = _create_csaf_root(csaf)

    vulnerabilities = []
    product_tree = CSAFProductTree(full_product_names=[])

    if product:
        vulnerabilities, product_tree = _get_data_for_product(
            product, parameters.vulnerability_names
        )
    else:
        vulnerabilities, product_tree = _get_data_for_vulnerabilities(
            parameters.vulnerability_names
        )

    if not vulnerabilities:
        return None

    csaf_content = CSAFContent(vulnerabilities, product_tree)
    content_json = jsonpickle.encode(csaf_content, unpicklable=False)
    content_hash = hashlib.sha256(
        content_json.casefold().encode("utf-8").strip()
    ).hexdigest()
    csaf.content_hash = content_hash
    csaf.document_id = csaf_root.document.tracking.id
    csaf.save()

    csaf_root.product_tree = product_tree
    csaf_root.vulnerabilities = vulnerabilities

    return csaf_root


def update_csaf_document(parameters: CSAFUpdateParameters) -> Optional[CSAFRoot]:
    try:
        csaf = CSAF.objects.get(document_base_id=parameters.document_base_id)
        csaf_vulnerability_names = list(
            CSAF_Vulnerability.objects.filter(csaf=csaf).values_list("name", flat=True)
        )
    except CSAF.DoesNotExist:
        raise NotFound(  # pylint: disable=raise-missing-from
            f"CSAF document with id {parameters.document_base_id} does not exist"
        )
        # The DoesNotExist exception itself is not relevant and must not be re-raised

    vulnerabilities = []
    product_tree = CSAFProductTree(full_product_names=[])

    if csaf.product:
        vulnerabilities, product_tree = _get_data_for_product(
            csaf.product, csaf_vulnerability_names
        )
    else:
        vulnerabilities, product_tree = _get_data_for_vulnerabilities(
            csaf_vulnerability_names
        )

    csaf_content = CSAFContent(vulnerabilities, product_tree)
    content_json = jsonpickle.encode(csaf_content, unpicklable=False)
    content_hash = hashlib.sha256(
        content_json.casefold().encode("utf-8").strip()
    ).hexdigest()

    if content_hash == csaf.content_hash:
        return None

    if parameters.publisher_name:
        csaf.publisher_name = parameters.publisher_name
    if parameters.publisher_category:
        csaf.publisher_category = parameters.publisher_category
    if parameters.publisher_namespace:
        csaf.publisher_namespace = parameters.publisher_namespace
    if parameters.tracking_status:
        csaf.tracking_status = parameters.tracking_status
    csaf.version += 1
    csaf.content_hash = content_hash
    csaf.save()

    CSAF_Revision.objects.create(
        csaf=csaf,
        date=csaf.tracking_current_release_date,
        version=csaf.version,
        summary="Update",
    )

    csaf_root = _create_csaf_root(csaf)

    csaf.document_id = csaf_root.document.tracking.id
    csaf.save()

    csaf_root.product_tree = product_tree
    csaf_root.vulnerabilities = vulnerabilities

    return csaf_root


def _get_document_id(
    document_id_prefix: str, document_base_id: str, document_version: int
) -> str:
    return document_id_prefix + "_" + document_base_id + f"_{document_version:04d}"


def _create_csaf_root(csaf: CSAF) -> CSAFRoot:
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

    csaf_revision_history_list = []
    csaf_revisions = CSAF_Revision.objects.filter(csaf=csaf)
    for csaf_revision in csaf_revisions:
        csaf_revision_history = CSAFRevisionHistory(
            date=csaf_revision.date.isoformat(),
            number=str(csaf_revision.version),
            summary=csaf_revision.summary,
        )
        csaf_revision_history_list.append(csaf_revision_history)

    document_id = _get_document_id(
        csaf.document_id_prefix, csaf.document_base_id, csaf.version
    )

    csaf_tracking = CSAFTracking(
        id=document_id,
        initial_release_date=csaf.tracking_initial_release_date.isoformat(),
        current_release_date=csaf.tracking_current_release_date.isoformat(),
        version=str(csaf.version),
        status=csaf.tracking_status,
        generator=csaf_generator,
        revision_history=csaf_revision_history_list,
    )

    csaf_tlp = CSAFTLP(label=csaf.tlp_label)
    csaf_distribution = CSAFDistribution(tlp=csaf_tlp)

    csaf_document = CSAFDocument(
        category="csaf_vex",
        csaf_version="2.0",
        title=csaf.title,
        publisher=csaf_publisher,
        tracking=csaf_tracking,
        distribution=csaf_distribution,
    )

    csaf_root = CSAFRoot(
        document=csaf_document,
        product_tree=None,
        vulnerabilities=[],
    )

    return csaf_root


def _get_data_for_vulnerabilities(vulnerability_names: list[str]) -> tuple:
    vulnerabilities = []
    product_tree = CSAFProductTree(full_product_names=[])
    for vulnerability_name in vulnerability_names:
        vulnerability = _create_vulnerability(vulnerability_name)
        vulnerabilities.append(vulnerability)
        current_vulnerability_description = None

        observations = get_observations_for_vulnerability(vulnerability_name)
        for observation in observations:
            current_vulnerability_description = _set_vulnerability_description(
                vulnerability, observation, current_vulnerability_description
            )

            full_product_name = CSAFFullProductName(
                name=observation.product.name,
                product_id=_get_product_id(observation.product),
            )
            if full_product_name not in product_tree.full_product_names:
                product_tree.full_product_names.append(full_product_name)

            _set_product_status(vulnerability, observation)
            _remove_conflicting_product_status(vulnerability)
            _set_remediation(vulnerability, observation)
            _set_flag_or_threat(vulnerability, observation)

    return vulnerabilities, product_tree


def _get_data_for_product(product: Product, vulnerability_names: list[str]) -> tuple:
    vulnerabilities: dict[str, CSAFVulnerability] = {}
    product_tree = CSAFProductTree(full_product_names=[])

    full_product_name = CSAFFullProductName(
        name=product.name,
        product_id=_get_product_id(product),
    )
    product_tree.full_product_names.append(full_product_name)

    observations = get_observations_for_product(product, vulnerability_names)
    for observation in observations:
        vulnerability = vulnerabilities.get(observation.vulnerability_id)
        if not vulnerability:
            vulnerability = _create_vulnerability(observation.vulnerability_id)
            vulnerabilities[observation.vulnerability_id] = vulnerability
            _set_vulnerability_description(vulnerability, observation, None)
        _set_product_status(vulnerability, observation)
        _remove_conflicting_product_status(vulnerability)
        _set_remediation(vulnerability, observation)
        _set_flag_or_threat(vulnerability, observation)

    return list(vulnerabilities.values()), product_tree


def _create_vulnerability(vulnerability_name) -> CSAFVulnerability:
    product_status = CSAFProductStatus(
        fixed=[], known_affected=[], known_not_affected=[], under_investigation=[]
    )
    if vulnerability_name.startswith("CVE"):
        vulnerability = CSAFVulnerability(
            cve=vulnerability_name,
            product_status=product_status,
            notes=[],
            flags=[],
            ids=[],
            references=[],
            remediations=[],
            threats=[],
        )
    else:
        vulnerability_id = CSAFId(
            text=vulnerability_name,
            system_name=get_vulnerability_ecosystem(vulnerability_name),
        )
        vulnerability = CSAFVulnerability(
            cve=None,
            product_status=product_status,
            notes=[],
            flags=[],
            ids=[vulnerability_id],
            references=[],
            remediations=[],
            threats=[],
        )
    reference_url = get_vulnerability_url(vulnerability_name)
    if reference_url:
        reference = CSAFReference(
            category="external", url=reference_url, summary="Security Advisory"
        )
        vulnerability.references.append(reference)

    return vulnerability


def _set_vulnerability_description(
    vulnerability: CSAFVulnerability,
    observation: Observation,
    current_vulnerability_description: Optional[str],
) -> str:
    if (
        not current_vulnerability_description
        or current_vulnerability_description == "No description available"
    ):
        description = (
            observation.description
            if observation.description
            else "No description available"
        )
        current_vulnerability_description = description
        csaf_note = CSAFNote(
            category="description",
            text=description,
        )
        vulnerability.notes.append(csaf_note)

    return current_vulnerability_description


def _set_product_status(vulnerability: CSAFVulnerability, observation: Observation):
    csaf_status = _map_status(observation.current_status)
    product_id = _get_product_id(observation.product)
    if csaf_status == CSAF_Status.CSAF_STATUS_NOT_AFFECTED:
        if product_id not in vulnerability.product_status.known_not_affected:
            vulnerability.product_status.known_not_affected.append(product_id)
    elif csaf_status == CSAF_Status.CSAF_STATUS_AFFECTED:
        if product_id not in vulnerability.product_status.known_affected:
            vulnerability.product_status.known_affected.append(product_id)
    elif csaf_status == CSAF_Status.CSAF_STATUS_FIXED:
        if product_id not in vulnerability.product_status.fixed:
            vulnerability.product_status.fixed.append(product_id)
    elif csaf_status == CSAF_Status.CSAF_STATUS_UNDER_INVESTIGATION:
        if product_id not in vulnerability.product_status.under_investigation:
            vulnerability.product_status.under_investigation.append(product_id)


def _remove_conflicting_product_status(vulnerability: CSAFVulnerability):
    product_ids = vulnerability.product_status.known_affected

    under_investigation_product_ids = []
    for product_id in vulnerability.product_status.under_investigation:
        if product_id not in product_ids:
            under_investigation_product_ids.append(product_id)
            product_ids.append(product_id)
    vulnerability.product_status.under_investigation = under_investigation_product_ids

    known_not_affected_product_ids = []
    for product_id in vulnerability.product_status.known_not_affected:
        if product_id not in product_ids:
            known_not_affected_product_ids.append(product_id)
            product_ids.append(product_id)
    vulnerability.product_status.known_not_affected = known_not_affected_product_ids

    fixed_product_ids = []
    for product_id in vulnerability.product_status.fixed:
        if product_id not in product_ids:
            fixed_product_ids.append(product_id)
            product_ids.append(product_id)
    vulnerability.product_status.fixed = fixed_product_ids


def _set_remediation(vulnerability: CSAFVulnerability, observation: Observation):
    csaf_status = _map_status(observation.current_status)
    if csaf_status == CSAF_Status.CSAF_STATUS_AFFECTED:
        product_id = _get_product_id(observation.product)
        category = "mitigation" if observation.recommendation else "none_available"
        details = (
            observation.recommendation
            if observation.recommendation
            else "No remediation available"
        )

        found = _check_and_append_none_available(vulnerability, product_id, category)

        found = _check_and_append_mitigation(
            found, vulnerability, product_id, category, details
        )

        if not found:
            remediation = CSAFRemediation(
                category=category,
                details=details,
                product_ids=[product_id],
            )
            vulnerability.remediations.append(remediation)

        # remove "none_available" remediation if mitigation is available
        if category == "mitigation":
            for remediation in vulnerability.remediations:
                if (
                    remediation.category == "none_available"
                    and product_id in remediation.product_ids
                ):
                    remediation.product_ids.remove(product_id)

        # remove remediations without product_ids
        remediations = []
        for remediation in vulnerability.remediations:
            if remediation.product_ids:
                remediations.append(remediation)
        vulnerability.remediations = remediations


def _check_and_append_none_available(
    vulnerability: CSAFVulnerability, product_id: str, category: str
) -> bool:
    found = False

    if category == "none_available":
        for remediation in vulnerability.remediations:
            if product_id in remediation.product_ids:
                found = True
                break

        if not found:
            for remediation in vulnerability.remediations:
                if (
                    remediation.category == "none_available"
                    and product_id not in remediation.product_ids
                ):
                    remediation.product_ids.append(product_id)
                    found = True
                    break

    return found


def _check_and_append_mitigation(
    found: bool,
    vulnerability: CSAFVulnerability,
    product_id: str,
    category: str,
    details: str,
) -> bool:
    if category == "mitigation":
        for remediation in vulnerability.remediations:
            if remediation.category == category and remediation.details == details:
                if product_id not in remediation.product_ids:
                    remediation.product_ids.append(product_id)
                found = True
                break

    return found


def _set_flag_or_threat(vulnerability: CSAFVulnerability, observation: Observation):
    csaf_status = _map_status(observation.current_status)
    if csaf_status == CSAF_Status.CSAF_STATUS_NOT_AFFECTED:
        product_id = _get_product_id(observation.product)
        try:
            observation_log = Observation_Log.objects.filter(
                observation=observation
            ).latest("created")
        except Observation_Log.DoesNotExist:
            observation_log = None
        category = "impact"
        details = (
            observation_log.comment
            if observation_log and observation_log.comment
            else "No justification available"
        )
        found = False
        for threat in vulnerability.threats:
            if threat.category == category and threat.details == details:
                if product_id not in threat.product_ids:
                    threat.product_ids.append(product_id)
                found = True
                break
        if not found:
            threat = CSAFThreat(
                category=category,
                details=details,
                product_ids=[product_id],
            )
            vulnerability.threats.append(threat)


def _map_status(secobserve_status: str) -> Optional[str]:
    if secobserve_status in (Status.STATUS_OPEN, Status.STATUS_RISK_ACCEPTED):
        return CSAF_Status.CSAF_STATUS_AFFECTED

    if secobserve_status == Status.STATUS_RESOLVED:
        return CSAF_Status.CSAF_STATUS_FIXED

    if secobserve_status in (
        Status.STATUS_NOT_AFFECTED,
        Status.STATUS_NOT_SECURITY,
        Status.STATUS_FALSE_POSITIVE,
    ):
        return CSAF_Status.CSAF_STATUS_NOT_AFFECTED

    if secobserve_status == Status.STATUS_IN_REVIEW:
        return CSAF_Status.CSAF_STATUS_UNDER_INVESTIGATION

    if secobserve_status == Status.STATUS_DUPLICATE:
        return None

    raise ValueError(f"Invalid status {secobserve_status}")


def _get_product_id(product: Product) -> str:
    return product.name
