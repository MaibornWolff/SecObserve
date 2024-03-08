import hashlib
from dataclasses import dataclass
from typing import Optional

import jsonpickle
from rest_framework.exceptions import NotFound

from application.__init__ import __version__
from application.commons.services.global_request import get_current_user
from application.core.models import Branch, Observation, Observation_Log, Product
from application.core.types import Status
from application.vex.models import CSAF, CSAF_Branch, CSAF_Revision, CSAF_Vulnerability
from application.vex.queries.csaf import get_csaf_by_document_id
from application.vex.services.csaf_helpers import get_vulnerability_ecosystem
from application.vex.services.vex_base import (
    check_and_get_product,
    check_branch_names,
    check_product_or_vulnerabilities,
    check_vulnerability_names,
    create_document_base_id,
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
    CSAFFlag,
    CSAFFullProductName,
    CSAFGenerator,
    CSAFId,
    CSAFNote,
    CSAFProductBranch,
    CSAFProductIdentificationHelper,
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
    CSF_Branch_Category,
)


@dataclass()
class CSAFCreateParameters:
    product_id: int
    vulnerability_names: list[str]
    branch_names: list[str]
    document_id_prefix: str
    title: str
    publisher_name: str
    publisher_category: str
    publisher_namespace: str
    tracking_status: str
    tlp_label: str


@dataclass()
class CSAFUpdateParameters:
    document_id_prefix: str
    document_base_id: str
    publisher_name: str
    publisher_category: str
    publisher_namespace: str
    tracking_status: str
    tlp_label: str


@dataclass()
class CSAFContent:
    vulnerabilities: list[CSAFVulnerability]
    product_tree: CSAFProductTree


def create_csaf_document(parameters: CSAFCreateParameters) -> Optional[CSAFRoot]:
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

    csaf = CSAF.objects.create(
        product=product,
        document_id_prefix=parameters.document_id_prefix,
        document_base_id=document_base_id,
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

    for branch in branches:
        CSAF_Branch.objects.create(csaf=csaf, branch=branch)

    csaf_root = _create_csaf_root(csaf)

    vulnerabilities = []
    product_tree = CSAFProductTree(branches=[])

    if product:
        vulnerabilities, product_tree = _get_content_for_product(
            product, parameters.vulnerability_names, branches
        )
    else:
        vulnerabilities, product_tree = _get_content_for_vulnerabilities(
            parameters.vulnerability_names
        )

    if not vulnerabilities:
        csaf.delete()
        return None

    csaf_content = CSAFContent(vulnerabilities, product_tree)
    content_json = jsonpickle.encode(csaf_content, unpicklable=False)
    content_hash = hashlib.sha256(
        content_json.casefold().encode("utf-8").strip()
    ).hexdigest()
    csaf.content_hash = content_hash
    csaf.save()

    csaf_root.product_tree = product_tree
    csaf_root.vulnerabilities = vulnerabilities

    return csaf_root


def update_csaf_document(parameters: CSAFUpdateParameters) -> Optional[CSAFRoot]:
    csaf = get_csaf_by_document_id(
        parameters.document_id_prefix, parameters.document_base_id
    )
    if not csaf:
        raise NotFound(
            f"CSAF document with ids {parameters.document_id_prefix} and {parameters.document_base_id} does not exist"
        )

    csaf_vulnerability_names = list(
        CSAF_Vulnerability.objects.filter(csaf=csaf).values_list("name", flat=True)
    )

    csaf_branch_ids = CSAF_Branch.objects.filter(csaf=csaf).values_list(
        "branch", flat=True
    )
    csaf_branches = list(Branch.objects.filter(id__in=csaf_branch_ids))

    vulnerabilities = []
    product_tree = CSAFProductTree(branches=[])

    if csaf.product:
        vulnerabilities, product_tree = _get_content_for_product(
            csaf.product, csaf_vulnerability_names, csaf_branches
        )
    else:
        vulnerabilities, product_tree = _get_content_for_vulnerabilities(
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
    if parameters.tlp_label:
        csaf.tlp_label = parameters.tlp_label
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

    tracking_id = _get_document_id(
        csaf.document_id_prefix, csaf.document_base_id, csaf.version
    )

    csaf_tracking = CSAFTracking(
        id=tracking_id,
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


def _get_content_for_vulnerabilities(vulnerability_names: list[str]) -> tuple:
    vulnerabilities = []
    product_tree = CSAFProductTree(branches=[])
    for vulnerability_name in vulnerability_names:
        vulnerability = _create_vulnerability(vulnerability_name)
        vulnerabilities.append(vulnerability)
        current_vulnerability_description = None

        observations = get_observations_for_vulnerability(vulnerability_name)
        for observation in observations:
            current_vulnerability_description = _set_vulnerability_description(
                vulnerability, observation, current_vulnerability_description
            )
            _append_to_product_tree(
                product_tree, observation.product, observation.branch
            )

            _set_product_status(vulnerability, observation)
            _remove_conflicting_product_status(vulnerability)
            _set_remediation(vulnerability, observation)
            _set_flag_or_threat(vulnerability, observation)

    return vulnerabilities, product_tree


def _get_content_for_product(
    product: Product, vulnerability_names: list[str], branches: list[Branch]
) -> tuple:
    vulnerabilities: dict[str, CSAFVulnerability] = {}
    product_tree = CSAFProductTree(branches=[])

    product_has_branches = False
    if branches:
        for branch in branches:
            product_has_branches = True
            _append_to_product_tree(product_tree, product, branch)
    else:
        for branch in Branch.objects.filter(product=product):
            product_has_branches = True
            _append_to_product_tree(product_tree, product, branch)

    if not product_has_branches:
        _append_to_product_tree(product_tree, product, None)

    observations = get_observations_for_product(product, vulnerability_names, branches)
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


def _create_product(product: Product, branch: Optional[Branch]) -> CSAFFullProductName:
    product_identification_helper = None
    if branch:
        if branch.purl or branch.cpe23:
            purl = branch.purl if branch.purl else None
            cpe = branch.cpe23 if branch.cpe23 else None
            product_identification_helper = CSAFProductIdentificationHelper(
                purl=purl, cpe=cpe
            )
    else:
        if product.purl or product.cpe23:
            purl = product.purl if product.purl else None
            cpe = product.cpe23 if product.cpe23 else None
            product_identification_helper = CSAFProductIdentificationHelper(
                purl=purl, cpe=cpe
            )

    product_name = f"{product.name}:{branch.name}" if branch else product.name

    full_product_name = CSAFFullProductName(
        name=product_name,
        product_id=_get_product_id(product, branch),
        product_identification_helper=product_identification_helper,
    )

    return full_product_name


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
    product_id = _get_product_id(observation.product, observation.branch)
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
    product_ids = []

    for product_id in vulnerability.product_status.known_affected:
        product_ids.append(product_id)

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
        product_id = _get_product_id(observation.product, observation.branch)
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
        product_id = _get_product_id(observation.product, observation.branch)
        try:
            observation_log = Observation_Log.objects.filter(
                observation=observation
            ).latest("created")
        except Observation_Log.DoesNotExist:
            observation_log = None

        if observation_log and observation_log.vex_justification:
            found = False
            for flag in vulnerability.flags:
                if flag.label == observation_log.vex_justification:
                    if product_id not in flag.product_ids:
                        flag.product_ids.append(product_id)
                    found = True
                    break
            if not found:
                csaf_flag = CSAFFlag(
                    label=observation_log.vex_justification,
                    product_ids=[product_id],
                )
                vulnerability.flags.append(csaf_flag)
        else:
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


def _get_product_id(product: Product, branch: Optional[Branch]) -> str:
    if branch:
        if branch.purl:
            return branch.purl
        if branch.cpe23:
            return branch.cpe23
        return f"{product.name}:{branch.name}"

    if product.purl:
        return product.purl
    if product.cpe23:
        return product.cpe23
    return product.name


def _append_to_product_tree(
    product_tree: CSAFProductTree,
    product: Product,
    branch: Optional[Branch],
) -> None:

    found = False
    for product_family_branch in product_tree.branches:
        if product_family_branch.name == product.name:
            found = True
            break
    if not found:
        product_family_branch = CSAFProductBranch(
            name=product.name,
            category=CSF_Branch_Category.CSAF_BRANCH_CATEGORY_PRODUCT_FAMILY,
            branches=[],
        )
        product_tree.branches.append(product_family_branch)

    if not branch:
        if product_family_branch.branches is None:
            raise ValueError("Product family branches should not be None")
        for product_name_branch in product_family_branch.branches:
            if product_name_branch.name == product.name:
                return

        new_product_full_name = _create_product(product, branch)
        new_product_branch = CSAFProductBranch(
            name=product.name,
            category=CSF_Branch_Category.CSAF_BRANCH_CATEGORY_PRODUCT_NAME,
            product=new_product_full_name,
        )
        product_family_branch.branches.append(new_product_branch)
    else:
        if product_family_branch.branches is None:
            raise ValueError("Product family branches should not be None")
        for version_branch in product_family_branch.branches:
            if version_branch.name == f"{product.name}:{branch.name}":
                return

        new_product_full_name = _create_product(product, branch)
        new_product_branch = CSAFProductBranch(
            name=f"{product.name}:{branch.name}",
            category=CSF_Branch_Category.CSAF_BRANCH_CATEGORY_PRODUCT_VERSION,
            product=new_product_full_name,
        )
        product_family_branch.branches.append(new_product_branch)
