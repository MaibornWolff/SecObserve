from typing import Optional

from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.vex.models import CSAF, CSAF_Vulnerability


def get_csafs() -> QuerySet[CSAF]:
    user = get_current_user()

    if user is None:
        return CSAF.objects.none()

    if user.is_superuser:
        return CSAF.objects.all()

    return CSAF.objects.filter(user=user)


def get_csaf_by_document_base_id(document_base_id: str) -> Optional[CSAF]:
    user = get_current_user()

    if user is None:
        return None

    if user.is_superuser:
        try:
            return CSAF.objects.get(document_base_id=document_base_id)
        except CSAF.DoesNotExist:
            return None

    try:
        return CSAF.objects.get(document_base_id=document_base_id, user=user)
    except CSAF.DoesNotExist:
        return None

def get_csaf_vulnerabilities() -> QuerySet[CSAF_Vulnerability]:
    user = get_current_user()

    if user is None:
        return CSAF_Vulnerability.objects.none()

    if user.is_superuser:
        return CSAF_Vulnerability.objects.all()

    return CSAF_Vulnerability.objects.filter(csaf__in=get_csafs()).order_by("name")
