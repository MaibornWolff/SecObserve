from rest_framework.exceptions import ValidationError

from application.core.api.serializers_helpers import validate_purl
from application.vex.models import VEX_Document, VEX_Statement
from application.vex.types import OpenVEX_Status, VEX_Document_Type, VEX_Status


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
        raise ValidationError("OpenVEX document doesn't contain any statements")
    if not isinstance(statements, list):
        raise ValidationError("statements is not a list")

    statement_counter = 0
    for statement in statements:
        if not isinstance(statement, dict):
            raise ValidationError(f"statement[{statement_counter}] is not a dictionary")
        vulnerability_id = statement.get("vulnerability", {}).get("name")
        if not vulnerability_id:
            raise ValidationError(f"vulnerability[{statement_counter}]/name is missing")
        description = statement.get("vulnerability", {}).get("description")
        status = statement.get("status")
        if not status:
            raise ValidationError(f"status[{statement_counter}] is missing")
        if (status, status) not in VEX_Status.VEX_STATUS_CHOICES:
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
                f"statement[{statement_counter}] doesn't contain any products"
            )
        if not isinstance(products, list):
            raise ValidationError(f"products[{statement_counter}] is not a list")

        product_counter = 0
        for product in products:
            if not isinstance(product, dict):
                raise ValidationError(
                    f"product[{statement_counter}][{product_counter}] is not a dictionary"
                )
            product_purl = product.get("identifiers", {}).get("purl", "")
            if product_purl:
                validate_purl(product_purl)
            else:
                product_purl = product.get("@id", "")
                validate_purl(product_purl)

            components = product.get("subcomponents", [])
            if not components:
                VEX_Statement.objects.create(
                    document=openvex_document,
                    vulnerability_id=vulnerability_id,
                    description=description,
                    status=status,
                    justification=justification,
                    impact=impact,
                    remediation=remediation,
                    product_purl=product_purl,
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
                component_purl = component.get("identifiers", {}).get("purl", "")
                if component_purl:
                    validate_purl(component_purl)
                else:
                    component_purl = product.get("@id", "")
                    validate_purl(component_purl)

                VEX_Statement.objects.create(
                    document=openvex_document,
                    vulnerability_id=vulnerability_id,
                    description=description,
                    status=status,
                    justification=justification,
                    impact=impact,
                    remediation=remediation,
                    product_purl=product_purl,
                    component_purl=component_purl,
                )

                component_counter += 1
            product_counter += 1
        statement_counter += 1
