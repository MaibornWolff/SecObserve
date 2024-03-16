from typing import Optional

from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.core.models import Product_Member
from application.vex.models import OpenVEX, OpenVEX_Branch, OpenVEX_Vulnerability


def get_open_vex_s() -> QuerySet[OpenVEX]:
    user = get_current_user()

    if user is None:
        return OpenVEX.objects.none()

    open_vex_s = OpenVEX.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("product__product_group"), user=user
        )

        open_vex_s = open_vex_s.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
        )

        open_vex_s = open_vex_s.filter(
            Q(product__member=True)
            | Q(product__product_group__member=True)
            | (Q(product__isnull=True) & Q(user=user))
        )

    return open_vex_s


def get_open_vex_by_document_id(
    document_id_prefix: str, document_base_id: str
) -> Optional[OpenVEX]:
    user = get_current_user()

    if user is None:
        return None

    try:
        open_vex = OpenVEX.objects.get(
            document_id_prefix=document_id_prefix,
            document_base_id=document_base_id,
        )
        if not user.is_superuser and open_vex not in get_open_vex_s():
            return None
        return open_vex
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
