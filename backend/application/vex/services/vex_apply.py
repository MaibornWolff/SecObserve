import logging

from packageurl import PackageURL

from application.core.models import Observation
from application.vex.models import VEX_Document, VEX_Statement

logger = logging.getLogger("secobserve.vex")


def apply_vex_for_observation(observation: Observation) -> None:
    purl_str = observation.branch.purl if observation.branch else None
    if not purl_str:
        purl_str = observation.product.purl
    if not purl_str:
        return

    try:
        purl = PackageURL.from_string(purl_str)
    except ValueError as e:
        logger.warning(
            f"Failed to parse SecObserve product's PackageURL from string '{purl_str}': {e}"
        )
        return

    if purl.namespace:
        search_purl = f"pkg:{purl.type}/{purl.namespace}/{purl.name}"
    else:
        search_purl = f"pkg:{purl.type}/{purl.name}"
    if purl.version:
        search_purl += f"@{purl.version}"

    narrowed_candidates = []
    vex_statement_candidates = VEX_Statement.objects.filter(
        product_purl__startswith=search_purl
    )
    for candidate in vex_statement_candidates:
        try:
            candidate_purl = PackageURL.from_string(candidate.product_purl)
        except ValueError as e:
            logger.warning(
                f"Failed to parse VEX product`s PackageURL from string '{candidate.product_purl}': {e}"
            )
            continue

        if not _match_purl(purl, candidate_purl):
            continue

        if candidate.component_purl:
            if not observation.origin_component_purl:
                continue

            try:
                origin_component_purl = PackageURL.from_string(
                    observation.origin_component_purl
                )
            except ValueError as e:
                logger.warning(
                    "Failed to parse SecObserve component's "
                    f"PackageURL from string '{observation.origin_component_purl}': {e}"
                )
                continue

            try:
                candidate_component_purl = PackageURL.from_string(
                    candidate.component_purl
                )
            except ValueError as e:
                logger.warning(
                    f"Failed to parse VEX component's PackageURL from string '{candidate.component_purl}': {e}"
                )
                continue

            if not _match_purl(origin_component_purl, candidate_component_purl):
                continue

        narrowed_candidates.append(candidate)


def apply_vex_for_document(vex_document: VEX_Document) -> None:
    pass


def _match_purl(purl: PackageURL, candidate_purl: PackageURL) -> bool:
    if purl.namespace != candidate_purl.namespace:
        return False
    if purl.name != candidate_purl.name:
        return False
    if purl.type != candidate_purl.type:
        return False
    if purl.version and purl.version != candidate_purl.version:
        return False
    if purl.subpath and purl.subpath != candidate_purl.subpath:
        return False

    # All qualifiers in the purl must be present in the candidate_purl
    if purl.qualifiers:
        if not candidate_purl.qualifiers:
            return False
        if isinstance(purl.qualifiers, str):
            if candidate_purl.qualifiers != purl.qualifiers:
                return False
        if isinstance(purl.qualifiers, dict):
            if not isinstance(candidate_purl.qualifiers, dict):
                return False
            for key, value in purl.qualifiers.items():
                if candidate_purl.qualifiers.get(key) != value:
                    return False

    return True
