from typing import Optional

from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.vex.models import OpenVEX, OpenVEX_Branch, OpenVEX_Vulnerability


def get_open_vex_s() -> QuerySet[OpenVEX]:
    user = get_current_user()

    if user is None:
        return OpenVEX.objects.none()

    if user.is_superuser:
        return OpenVEX.objects.all()

    return OpenVEX.objects.filter(user=user)


def get_open_vex_by_document_id(
    document_id_prefix: str, document_base_id: str
) -> Optional[OpenVEX]:
    user = get_current_user()

    if user is None:
        return None

    if user.is_superuser:
        try:
            return OpenVEX.objects.get(
                document_id_prefix=document_id_prefix, document_base_id=document_base_id
            )
        except OpenVEX.DoesNotExist:
            return None

    try:
        return OpenVEX.objects.get(
            document_id_prefix=document_id_prefix,
            document_base_id=document_base_id,
            user=user,
        )
    except OpenVEX.DoesNotExist:
        return None


def get_open_vex_vulnerabilities() -> QuerySet[OpenVEX_Vulnerability]:
    user = get_current_user()

    if user is None:
        return OpenVEX_Vulnerability.objects.none()

    if user.is_superuser:
        return OpenVEX_Vulnerability.objects.all().order_by("name")

    return OpenVEX_Vulnerability.objects.filter(openvex__in=get_open_vex_s()).order_by(
        "name"
    )


def get_open_vex_branches() -> QuerySet[OpenVEX_Branch]:
    user = get_current_user()

    if user is None:
        return OpenVEX_Branch.objects.none()

    if user.is_superuser:
        return OpenVEX_Branch.objects.all().order_by("branch__name")

    return OpenVEX_Branch.objects.filter(openvex__in=get_open_vex_s()).order_by(
        "branch__name"
    )
