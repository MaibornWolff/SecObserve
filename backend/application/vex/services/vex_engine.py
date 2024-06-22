from typing import Optional

from packageurl import PackageURL

from application.commons.services.global_request import get_current_user
from application.core.models import Branch, Observation, Product
from application.core.services.observation import (
    get_current_status,
    get_current_vex_justification,
)
from application.core.services.observation_log import create_observation_log
from application.core.types import Assessment_Status, Status
from application.issue_tracker.services.issue_tracker import (
    push_observation_to_issue_tracker,
)
from application.vex.models import VEX_Statement
from application.vex.types import VEX_Status


class VEX_Engine:
    def __init__(self, product: Product, branch: Optional[Branch]):
        self.product = product
        self.branch = branch
        self.vex_statements: list[VEX_Statement] = []

        product_purl = branch.purl if branch and branch.purl else product.purl
        if not product_purl:
            return

        try:
            purl = PackageURL.from_string(product_purl)
        except ValueError:
            return

        search_purl = PackageURL(
            type=purl.type, namespace=purl.namespace, name=purl.name
        ).to_string()

        self.vex_statements = list(
            VEX_Statement.objects.filter(product_purl__startswith=search_purl)
        )

    def apply_vex_statements_for_observation(self, observation: Observation) -> None:
        previous_vex_statement = (
            observation.vex_statement if observation.vex_statement else None
        )
        observation.vex_statement = None

        vex_statement_found = False
        for vex_statement in self.vex_statements:
            vex_statement_found = apply_vex_statement_for_observation(
                vex_statement, observation, previous_vex_statement
            )
            if vex_statement_found:
                break

        # Write observation and observation log if no vex_statement was found but there was one before
        if not vex_statement_found and (
            previous_vex_statement != observation.vex_statement
            or observation.vex_status
        ):
            write_observation_log_no_vex_statement(observation, previous_vex_statement)


def apply_vex_statement_for_observation(
    vex_statement: VEX_Statement,
    observation: Observation,
    previous_vex_statement: Optional[VEX_Statement],
) -> bool:
    if vex_statement.vulnerability_id == observation.vulnerability_id and _match_purls(
        vex_statement, observation
    ):
        previous_current_status = observation.current_status
        previous_vex_status = observation.vex_status
        observation.vex_status = _get_secobserve_status(vex_statement.status)
        observation.current_status = get_current_status(observation)

        previous_current_vex_justification = observation.current_vex_justification
        previous_vex_vex_justification = observation.vex_vex_justification
        observation.vex_vex_justification = vex_statement.justification
        observation.current_vex_justification = get_current_vex_justification(
            observation
        )

        observation.vex_statement = vex_statement

        # Write observation and observation and push to issue tracker log if something has been changed
        if (  # pylint: disable=too-many-boolean-expressions
            (
                previous_current_status != observation.current_status
                or previous_vex_status != observation.vex_status
                or previous_vex_statement != observation.vex_statement
                or previous_vex_vex_justification != observation.vex_vex_justification
                or previous_current_vex_justification
                != observation.current_vex_justification
            )
            and not previous_vex_status == Status.STATUS_OPEN
            and not observation.vex_status == Status.STATUS_OPEN
            and not observation.current_status == Status.STATUS_OPEN
        ):
            _write_observation_log(
                observation,
                vex_statement,
                previous_current_status,
                previous_current_vex_justification,
            )
            push_observation_to_issue_tracker(observation, get_current_user())
        return True

    return False


def _match_purls(vex_statement: VEX_Statement, observation: Observation) -> bool:
    product_purl = (
        observation.branch.purl
        if observation.branch and observation.branch.purl
        else observation.product.purl
    )
    if not _match_purl(vex_statement.product_purl, product_purl):
        return False
    if not vex_statement.component_purl:
        return True
    return _match_purl(vex_statement.component_purl, observation.origin_component_purl)


def _match_purl(
    vex_purl_str: Optional[str], observation_purl_str: Optional[str]
) -> bool:
    if not vex_purl_str and not observation_purl_str:
        return True

    if not vex_purl_str or not observation_purl_str:
        return False

    try:
        vex_purl = PackageURL.from_string(vex_purl_str)
        observation_purl = PackageURL.from_string(observation_purl_str)
    except ValueError:
        return False

    if (  # pylint: disable=too-many-boolean-expressions
        vex_purl.type != observation_purl.type
        or vex_purl.namespace != observation_purl.namespace
        or vex_purl.name != observation_purl.name
        or (
            vex_purl.version
            and observation_purl.version
            and vex_purl.version != observation_purl.version
        )
        or (
            vex_purl.subpath
            and observation_purl.subpath
            and vex_purl.subpath != observation_purl.subpath
        )
        or not _check_qualifiers(vex_purl.qualifiers, observation_purl.qualifiers)
    ):
        return False

    return True


def _check_qualifiers(
    vex_qualifiers: Optional[str | dict], observation_qualifiers: Optional[str | dict]
) -> bool:
    if not vex_qualifiers and not observation_qualifiers:
        return True

    if not vex_qualifiers or not observation_qualifiers:
        return True

    if isinstance(vex_qualifiers, str) and isinstance(observation_qualifiers, str):
        return vex_qualifiers == observation_qualifiers

    if isinstance(vex_qualifiers, dict) and isinstance(observation_qualifiers, dict):
        for key, value in vex_qualifiers.items():
            if (
                observation_qualifiers.get(key) is not None
                and observation_qualifiers.get(key) != value
            ):
                return False
        for key, value in observation_qualifiers.items():
            if vex_qualifiers.get(key) is not None and vex_qualifiers.get(key) != value:
                return False
        return True

    return False


def _get_secobserve_status(vex_status: str) -> str:
    if vex_status == VEX_Status.VEX_STATUS_NOT_AFFECTED:
        return Status.STATUS_NOT_AFFECTED
    if vex_status == VEX_Status.VEX_STATUS_FIXED:
        return Status.STATUS_RESOLVED
    if vex_status == VEX_Status.VEX_STATUS_UNDER_INVESTIGATION:
        return Status.STATUS_IN_REVIEW
    return Status.STATUS_OPEN


def _write_observation_log(
    observation: Observation,
    vex_statement: VEX_Statement,
    previous_status: str,
    previous_vex_justification: str,
) -> None:
    if previous_status != observation.current_status:
        status = observation.current_status
    else:
        status = ""

    if previous_vex_justification != observation.current_vex_justification:
        vex_justification = observation.current_vex_justification
    else:
        vex_justification = ""

    comment = f"Updated by VEX statement from {vex_statement.document.document_id}"

    if vex_statement.impact:
        comment = f"{comment}\n\n{vex_statement.impact}"

    create_observation_log(
        observation,
        "",
        status,
        comment,
        vex_justification,
        Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
    )


def write_observation_log_no_vex_statement(
    observation: Observation,
    previous_vex_statement: Optional[VEX_Statement],
) -> None:
    observation.vex_status = ""
    previous_status = observation.current_status
    observation.current_status = get_current_status(observation)

    observation.vex_vex_justification = ""
    previous_vex_justification = observation.current_vex_justification
    observation.current_vex_justification = get_current_vex_justification(observation)

    log_status = (
        observation.current_status
        if previous_status != observation.current_status
        else ""
    )
    log_vex_justification = (
        observation.current_vex_justification
        if previous_vex_justification != observation.current_vex_justification
        else ""
    )

    if previous_vex_statement:
        log_comment = (
            f"Removed VEX statement from {previous_vex_statement.document.document_id}"
        )
    else:
        log_comment = "Removed unkown VEX statement"

    create_observation_log(
        observation,
        "",
        log_status,
        log_comment,
        log_vex_justification,
        Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
    )


def apply_vex_statements_after_import(
    product_purls: set[str], vex_statements: set[VEX_Statement]
) -> None:
    for product_purl in product_purls:
        try:
            purl = PackageURL.from_string(product_purl)
        except ValueError:
            continue

        search_purl = PackageURL(
            type=purl.type, namespace=purl.namespace, name=purl.name
        ).to_string()

        products = set(Product.objects.filter(purl__startswith=search_purl))
        branches = Branch.objects.filter(purl__startswith=search_purl)
        for branch in branches:
            products.add(branch.product)

        for product in products:
            observations = Observation.objects.filter(product=product)
            for observation in observations:
                for vex_statement in vex_statements:
                    apply_vex_statement_for_observation(
                        vex_statement, observation, observation.vex_statement
                    )
