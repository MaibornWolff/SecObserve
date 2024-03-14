from typing import Optional

from application.core.models import Observation
from application.vex.services.csaf_helpers import get_product_id, get_relationship_name
from application.vex.types import (
    CSAF_Branch_Category,
    CSAF_Relationship_Category,
    CSAFFullProductName,
    CSAFProductBranch,
    CSAFProductIdentificationHelper,
    CSAFProductRelationship,
    CSAFProductTree,
)


def get_component_id(
    component_name_version: str, purl: Optional[str], cpe: Optional[str]
) -> str:
    return purl if purl else cpe if cpe else component_name_version


def append_component_to_product_tree(
    product_tree: CSAFProductTree,
    observation: Observation,
) -> None:
    if not observation.origin_component_name_version:
        return

    components_branch_name = "_components_"

    found = False
    for components_branch in product_tree.branches:
        if components_branch.name == components_branch_name:
            found = True
            break
    if not found:
        components_branch = CSAFProductBranch(
            name=components_branch_name,
            category=CSAF_Branch_Category.CSAF_BRANCH_CATEGORY_PRODUCT_FAMILY,
            branches=[],
        )
        product_tree.branches.append(components_branch)

    if not components_branch.branches:
        components_branch.branches = []

    for component_branch in components_branch.branches:
        if component_branch.name == observation.origin_component_name_version:
            return

    component_branch = CSAFProductBranch(
        name=observation.origin_component_name_version,
        category=CSAF_Branch_Category.CSAF_BRANCH_CATEGORY_PRODUCT_VERSION,
        product=_create_component(
            observation.origin_component_name_version,
            observation.origin_component_purl,
            observation.origin_component_cpe,
        ),
    )
    components_branch.branches.append(component_branch)

    _append_component_to_relationships(product_tree, observation)


def _create_component(
    component_name_version: str, purl: Optional[str], cpe: Optional[str]
) -> CSAFFullProductName:
    product_identification_helper = None
    if purl or cpe:
        purl = purl if purl else None
        cpe = cpe if cpe else None
        product_identification_helper = CSAFProductIdentificationHelper(
            purl=purl, cpe=cpe
        )

    component_id = get_component_id(component_name_version, purl, cpe)
    full_product_name = CSAFFullProductName(
        name=component_name_version,
        product_id=component_id,
        product_identification_helper=product_identification_helper,
    )

    return full_product_name


def _append_component_to_relationships(
    product_tree: CSAFProductTree, observation: Observation
) -> None:
    if not observation.origin_component_name_version:
        return

    component_id = get_component_id(
        observation.origin_component_name_version,
        observation.origin_component_purl,
        observation.origin_component_cpe,
    )
    product_id = get_product_id(observation.product, observation.branch)

    for relationship in product_tree.relationships:
        if (
            relationship.product_reference == component_id
            and relationship.relates_to_product_reference == product_id
        ):
            return

    full_product_name = CSAFFullProductName(
        name=get_relationship_name(observation),
        product_id=get_relationship_name(observation),
    )

    relationship = CSAFProductRelationship(
        category=CSAF_Relationship_Category.CSAF_RELATIONSHIP_CATEGORY_DEFAULT_COMPONENT,
        product_reference=component_id,
        relates_to_product_reference=product_id,
        full_product_name=full_product_name,
    )
    product_tree.relationships.append(relationship)
