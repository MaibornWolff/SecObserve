from rest_framework.exceptions import ValidationError

from application.core.api.serializers_helpers import validate_cpe23, validate_purl
from application.vex.models import VEX_Document, VEX_Statement
from application.vex.types import OpenVEX_Status, VEX_Document_Type


def parse_openvex_data(data: dict) -> None:
    document_id = data.get("@id")
    if not document_id:
        raise ValidationError("@id is missing")
    version = data.get("version")
    if not version:
        raise ValidationError("version is missing")
    initial_release_date = data.get("timestamp")
    if not initial_release_date:
        raise ValidationError("timestamp is missing")
    current_release_date = data.get("last_updated")
    if not current_release_date:
        current_release_date = initial_release_date
    author = data.get("author")
    if not author:
        raise ValidationError("author is missing")
    role = data.get("role", "")

    try:
        openvex_document = VEX_Document.objects.get(
            document_id=document_id, author=author
        )
        openvex_document.delete()
    except VEX_Document.DoesNotExist:
        pass
    openvex_document = VEX_Document.objects.create(
        type=VEX_Document_Type.VEX_DOCUMENT_TYPE_OPENVEX,
        document_id=document_id,
        version=version,
        initial_release_date=initial_release_date,
        current_release_date=current_release_date,
        author=author,
        role=role,
    )

    statements = data.get("statements", [])
    if not statements:
        raise ValidationError("OpenVEX documenct doesn't contain statements")
    if not isinstance(statements, list):
        raise ValidationError("statements is not a list")

    statement_counter = 0
    for statement in statements:
        if not isinstance(statement, dict):
            raise ValidationError(f"statement[{statement_counter}] is not a dictionary")
        vulnerability_id = statement.get("vulnerability", {}).get("name")
        if not vulnerability_id:
            raise ValidationError(f"vulnerability[{statement_counter}]/name is missing")
        status = statement.get("status")
        if not status:
            raise ValidationError(f"status[{statement_counter}] is missing")
        if status not in OpenVEX_Status.OPENVEX_STATUS_LIST:
            raise ValidationError(f"status[{statement_counter}] is not valid: {status}")
        justification = statement.get("justification", "")
        impact = statement.get("impact_statement", "")
        if status == OpenVEX_Status.OPENVEX_STATUS_NOT_AFFECTED and not (
            justification or impact
        ):
            raise ValidationError(
                f"justification or impact_statement is required for status[{statement_counter}] not affected"
            )
        remediation = statement.get("action_statement", "")
        if status == OpenVEX_Status.OPENVEX_STATUS_AFFECTED and not remediation:
            raise ValidationError(
                f"action_statement is required for status[{statement_counter}] affected"
            )

        products = statement.get("products", [])
        if not products:
            raise ValidationError(
                f"statement[{statement_counter}] doesn't contain products"
            )
        if not isinstance(products, list):
            raise ValidationError(f"products[{statement_counter}] is not a list")

        product_counter = 0
        for product in products:
            if not isinstance(product, dict):
                raise ValidationError(
                    f"product[{statement_counter}][{product_counter}] is not a dictionary"
                )
            product_id = product.get("@id", "")
            product_purl = product.get("identifiers", {}).get("purl", "")
            if product_purl:
                validate_purl(product_purl)
            product_cpe23 = product.get("identifiers", {}).get("cpe23", "")
            if product_cpe23:
                validate_cpe23(product_cpe23)
            if not product_id and not product_purl and not product_cpe23:
                raise ValidationError(
                    f"product[{statement_counter}][{product_counter}] doesn't contain any valid identifier"
                )

            components = product.get("subcomponents", [])
            if not components:
                VEX_Statement.objects.create(
                    document=openvex_document,
                    vulnerability_id=vulnerability_id,
                    status=status,
                    justification=justification,
                    impact=impact,
                    remediation=remediation,
                    product_id=product_id,
                    product_purl=product_purl,
                    product_cpe23=product_cpe23,
                )
            elif not isinstance(components, list):
                raise ValidationError(
                    f"subcomponents[{statement_counter}][{product_counter}] is not a list"
                )

            component_counter = 0
            for component in components:
                if not isinstance(product, dict):
                    raise ValidationError(
                        f"subcomponent[{statement_counter}][{product_counter}][{component_counter}] is not a dictionary"
                    )
                component_id = component.get("@id", "")
                component_purl = component.get("identifiers", {}).get("purl", "")
                if component_purl:
                    validate_purl(component_purl)
                component_cpe23 = component.get("identifiers", {}).get("cpe23", "")
                if component_cpe23:
                    validate_cpe23(component_cpe23)
                if not component_id and not component_purl and not component_cpe23:
                    raise ValidationError(
                        f"subcomponent[{statement_counter}][{product_counter}][{component_counter}]"
                        " doesn't contain any valid identifier"
                    )
                VEX_Statement.objects.create(
                    document=openvex_document,
                    vulnerability_id=vulnerability_id,
                    status=status,
                    justification=justification,
                    impact=impact,
                    remediation=remediation,
                    product_id=product_id,
                    product_purl=product_purl,
                    product_cpe23=product_cpe23,
                    component_id=component_id,
                    component_purl=component_purl,
                    component_cpe23=component_cpe23,
                )

                component_counter += 1
            product_counter += 1
        statement_counter += 1
