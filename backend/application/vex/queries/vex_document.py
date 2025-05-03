from django.db.models.query import QuerySet

from application.access_control.services.current_user import get_current_user
from application.vex.models import VEX_Document, VEX_Statement


def get_vex_documents() -> QuerySet[VEX_Document]:
    user = get_current_user()

    if user is None:
        return VEX_Document.objects.none()

    if user.is_superuser:
        return VEX_Document.objects.all().order_by("document_id")

    return VEX_Document.objects.none()


def get_vex_statements() -> QuerySet[VEX_Statement]:
    user = get_current_user()

    if user is None:
        return VEX_Statement.objects.none()

    if user.is_superuser:
        return VEX_Statement.objects.all().order_by("vulnerability_id")

    return VEX_Statement.objects.none()
