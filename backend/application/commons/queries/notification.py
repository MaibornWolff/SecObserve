from django.db.models import Q
from django.db.models.query import QuerySet

from application.commons.models import Notification
from application.commons.services.global_request import get_current_user
from application.core.queries.product import get_products


def get_notifications() -> QuerySet[Notification]:
    user = get_current_user()

    if user is None:
        return Notification.objects.none()

    if user.is_superuser:
        return Notification.objects.all()

    products = get_products()

    return Notification.objects.filter(
        Q(product__in=products)
        & (Q(type=Notification.TYPE_SECURITY_GATE) | Q(type=Notification.TYPE_TASK))
    )
