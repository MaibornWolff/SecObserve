from dataclasses import dataclass
from typing import Optional

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.core.api.serializers_helpers import validate_purl
from application.core.types import VEX_Justification
from application.vex.models import VEX_Document, VEX_Statement
from application.vex.services.vex_engine import apply_vex_statements_after_import
from application.vex.types import (
    CycloneDX_Analysis_Justification,
    CycloneDX_Analysis_State,
    VEX_Document_Type,
    VEX_Status,
)


@dataclass
class CycloneDX_Analysis:
    state: str = ""
    justification: str = ""
    response: Optional[list[str]] = None
    detail: str = ""
    first_issued: str = ""
    last_updated: str = ""


@dataclass
class VexStatementData:
    vulnerability_id: str
    description: str
    status: str
    justification: str
    impact: str
    remediation: str
    product_purl: str
    component_purl: str = ""
    component_cyclonedx_bom_link: str = ""


def parse_cyclonedx_data(data: dict) -> None:
    cyclonedx_document = _create_cyclonedx_document(data)

    product_purls, vex_statements = _process_vex_statements(data, cyclonedx_document)

    apply_vex_statements_after_import(product_purls, vex_statements)


def _create_cyclonedx_document(data: dict) -> VEX_Document:
    document_id = data.get("serialNumber")
    if not document_id:
        raise ValidationError("serialNumber is missing")

    version = str(data.get("version", 1))

    metadata = data.get("metadata", {})

    timestamp = metadata.get("timestamp")
    if not timestamp:
        timestamp = timezone.now()

    author = None
    # Prefer authors list if available
    authors = metadata.get("authors")
    if authors and isinstance(authors, list) and len(authors) > 0:
        # Find the first author with a name set
        author = next(
            (item.get("name") for item in authors if isinstance(item, dict) and item.get("name")),
            None,
        )

    # Fall back to manufacturer or supplier if no authors
    if not author:
        author = metadata.get("manufacturer", {}).get("name") or metadata.get("supplier", {}).get("name")

    if not author:
        author = "Unknown"

    try:
        cyclonedx_document = VEX_Document.objects.get(document_id=document_id, author=author)
        cyclonedx_document.delete()
    except VEX_Document.DoesNotExist:
        pass

    cyclonedx_document = VEX_Document.objects.create(
        type=VEX_Document_Type.VEX_DOCUMENT_TYPE_CYCLONEDX,
        document_id=document_id,
        version=version,
        initial_release_date=timestamp,
        current_release_date=timestamp,
        author=author,
        role="",
    )

    return cyclonedx_document


def _process_vex_statements(data: dict, cyclonedx_document: VEX_Document) -> tuple[set[str], set[VEX_Statement]]:
    vulnerabilities = data.get("vulnerabilities", [])
    if not vulnerabilities:
        raise ValidationError("CycloneDX document doesn't contain any vulnerabilities")
    if not isinstance(vulnerabilities, list):
        raise ValidationError("vulnerabilities is not a list")

    components_map = _build_components_map(data)

    product_purl = data.get("metadata", {}).get("component", {}).get("purl", "")
    if product_purl:
        validate_purl(product_purl)

    product_purls: set[str] = set()
    vex_statements: set[VEX_Statement] = set()

    vulnerability_counter = 0
    for vulnerability in vulnerabilities:
        if not isinstance(vulnerability, dict):
            raise ValidationError(f"vulnerability[{vulnerability_counter}] is not a dictionary")

        vulnerability_id = vulnerability.get("id")
        if not vulnerability_id:
            raise ValidationError(f"vulnerability[{vulnerability_counter}]/id is missing")

        analysis = vulnerability.get("analysis", {})
        if not analysis:
            # Skip vulnerabilities without analysis
            vulnerability_counter += 1
            continue

        cyclonedx_analysis = _parse_analysis(analysis, vulnerability_counter)

        vex_status = _map_cyclonedx_state_to_vex_status(cyclonedx_analysis.state)
        if not vex_status:
            raise ValidationError(
                f"vulnerability[{vulnerability_counter}]/analysis/state is not valid: {cyclonedx_analysis.state}"
            )

        description = vulnerability.get("description", "")
        detail = vulnerability.get("detail", "")
        if detail:
            description += f"\n\n{detail}"

        remediation = _build_remediation_text(cyclonedx_analysis.response, vulnerability.get("recommendation", ""))

        affects = vulnerability.get("affects", [])
        if not affects:
            # General statement for the product
            _create_vex_statement(
                cyclonedx_document,
                product_purls,
                vex_statements,
                data=VexStatementData(
                    vulnerability_id=vulnerability_id,
                    description=description,
                    status=vex_status,
                    justification=cyclonedx_analysis.justification,
                    impact=cyclonedx_analysis.detail,
                    remediation=remediation,
                    product_purl=product_purl,
                ),
            )
        elif not isinstance(affects, list):
            raise ValidationError(f"affects[{vulnerability_counter}] is not a list")
        else:
            _process_affected_components(
                document=cyclonedx_document,
                product_purls=product_purls,
                vex_statements=vex_statements,
                vulnerability_counter=vulnerability_counter,
                vex_data=VexStatementData(
                    vulnerability_id=vulnerability_id,
                    description=description,
                    status=vex_status,
                    justification=cyclonedx_analysis.justification,
                    impact=cyclonedx_analysis.detail,
                    remediation=remediation,
                    product_purl=product_purl,
                ),
                affects=affects,
                components_map=components_map,
            )

        vulnerability_counter += 1

    return product_purls, vex_statements


def _build_components_map(data: dict) -> dict[str, dict]:
    components_map = {}

    # Add root component from metadata
    metadata_component = data.get("metadata", {}).get("component")
    if metadata_component and metadata_component.get("bom-ref"):
        components_map[metadata_component["bom-ref"]] = metadata_component

    # Add all components
    for component in data.get("components", []):
        if component.get("bom-ref"):
            components_map[component["bom-ref"]] = component

    return components_map


def _parse_analysis(analysis: dict, vulnerability_counter: int) -> CycloneDX_Analysis:
    state = analysis.get("state", "")
    if not state:
        raise ValidationError(f"vulnerability[{vulnerability_counter}]/analysis/state is missing")

    justification = analysis.get("justification", "")
    if justification:
        justification = _map_cyclonedx_justification_to_vex_justification(justification) or ""
    response = analysis.get("response", [])
    if not isinstance(response, list):
        response = []

    detail = analysis.get("detail", "")
    first_issued = analysis.get("firstIssued", "")
    last_updated = analysis.get("lastUpdated", "")

    return CycloneDX_Analysis(
        state=state,
        justification=justification,
        response=response,
        detail=detail,
        first_issued=first_issued,
        last_updated=last_updated,
    )


def _map_cyclonedx_state_to_vex_status(state: str) -> Optional[str]:
    mapping = {
        CycloneDX_Analysis_State.CYCLONEDX_STATE_RESOLVED: VEX_Status.VEX_STATUS_FIXED,
        CycloneDX_Analysis_State.CYCLONEDX_STATE_RESOLVED_WITH_PEDIGREE: VEX_Status.VEX_STATUS_FIXED,
        CycloneDX_Analysis_State.CYCLONEDX_STATE_EXPLOITABLE: VEX_Status.VEX_STATUS_AFFECTED,
        CycloneDX_Analysis_State.CYCLONEDX_STATE_IN_TRIAGE: VEX_Status.VEX_STATUS_UNDER_INVESTIGATION,
        CycloneDX_Analysis_State.CYCLONEDX_STATE_FALSE_POSITIVE: VEX_Status.VEX_STATUS_FALSE_POSITIVE,
        CycloneDX_Analysis_State.CYCLONEDX_STATE_NOT_AFFECTED: VEX_Status.VEX_STATUS_NOT_AFFECTED,
    }
    return mapping.get(state)


def _build_remediation_text(response: Optional[list[str]], recommendation: str) -> str:
    remediation_parts = []

    if response:
        response_text = ", ".join(response)
        remediation_parts.append(f"Response: {response_text}")

    if recommendation:
        remediation_parts.append(recommendation)

    return "; ".join(remediation_parts)


def _map_cyclonedx_justification_to_vex_justification(justification: str) -> Optional[str]:
    mapping = {
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_CODE_NOT_PRESENT: VEX_Justification.STATUS_VULNERABLE_CODE_NOT_PRESENT,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_CODE_NOT_REACHABLE: VEX_Justification.STATUS_VULNERABLE_CODE_NOT_IN_EXECUTE_PATH,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_REQUIRES_CONFIGURATION: VEX_Justification.STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_REQUIRES_DEPENDENCY: VEX_Justification.STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_REQUIRES_ENVIRONMENT: VEX_Justification.STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_PROTECTED_BY_COMPILER: VEX_Justification.STATUS_INLINE_MITIGATIONS_ALREADY_EXIST,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_PROTECTED_AT_RUNTIME: VEX_Justification.STATUS_INLINE_MITIGATIONS_ALREADY_EXIST,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_PROTECTED_AT_PERIMETER: VEX_Justification.STATUS_INLINE_MITIGATIONS_ALREADY_EXIST,  # noqa: E501 pylint: disable=line-too-long
        CycloneDX_Analysis_Justification.CYCLONEDX_JUSTIFICATION_PROTECTED_BY_MITIGATING_CONTROL: VEX_Justification.STATUS_INLINE_MITIGATIONS_ALREADY_EXIST,  # noqa: E501 pylint: disable=line-too-long
    }
    return mapping.get(justification)


def _process_affected_components(
    *,
    document: VEX_Document,
    product_purls: set[str],
    vex_statements: set[VEX_Statement],
    vulnerability_counter: int,
    vex_data: VexStatementData,
    affects: list,
    components_map: dict,
) -> None:
    affected_counter = 0
    for affected in affects:
        if not isinstance(affected, dict):
            raise ValidationError(f"affects[{vulnerability_counter}][{affected_counter}] is not a dictionary")

        ref = affected.get("ref")
        if not ref:
            raise ValidationError(f"affects[{vulnerability_counter}][{affected_counter}]/ref is missing")

        if ref.startswith("urn:cdx:"):
            component_purl = ""
            vex_data.product_purl = ""
            component_cyclonedx_bom_link = ref
        else:
            component_cyclonedx_bom_link = ""
            component = components_map.get(ref)
            if not component:
                raise ValidationError(
                    f"affects[{vulnerability_counter}][{affected_counter}]/ref '{ref}' not found in components"
                )

            component_purl = component.get("purl", "")
            if not component_purl:
                raise ValidationError(
                    f"affects[{vulnerability_counter}][{affected_counter}]/ref '{ref}' component is missing PURL"
                )
            validate_purl(component_purl)

            if not vex_data.product_purl:
                raise ValidationError("metadata/component/purl is missing for VEX data inside an SBOM")

        _create_vex_statement(
            document,
            product_purls,
            vex_statements,
            data=VexStatementData(
                vulnerability_id=vex_data.vulnerability_id,
                description=vex_data.description,
                status=vex_data.status,
                justification=vex_data.justification,
                impact=vex_data.impact,
                remediation=vex_data.remediation,
                product_purl=vex_data.product_purl,
                component_purl=component_purl,
                component_cyclonedx_bom_link=component_cyclonedx_bom_link,
            ),
        )

        affected_counter += 1


def _create_vex_statement(
    document: VEX_Document,
    product_purls: set[str],
    vex_statements: set[VEX_Statement],
    data: VexStatementData,
) -> None:
    vex_statement = VEX_Statement(
        document=document,
        vulnerability_id=data.vulnerability_id,
        description=data.description,
        status=data.status,
        justification=data.justification,
        impact=data.impact,
        remediation=data.remediation,
        product_purl=data.product_purl,
        component_purl=data.component_purl,
        component_cyclonedx_bom_link=data.component_cyclonedx_bom_link,
    )
    vex_statement.save()
    vex_statements.add(vex_statement)
    product_purls.add(data.product_purl)
