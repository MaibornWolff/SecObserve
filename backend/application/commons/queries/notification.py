from django.db.models.query import QuerySet

from application.commons.models import Notification
from application.commons.services.global_request import get_current_user


def get_notifications() -> QuerySet[Notification]:
    user = get_current_user()

    if user is None:
        return Notification.objects.none()

    if user.is_superuser:
        return Notification.objects.all()

    return Notification.objects.filter(user=user)
