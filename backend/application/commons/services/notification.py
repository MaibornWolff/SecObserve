from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from application.commons.models import Notification
from application.commons.queries.notification import get_notifications


def bulk_delete(notification_ids: list[int]) -> None:
    notifications = _check_notifications(notification_ids)
    notifications.delete()


def _check_notifications(notification_ids: list[int]) -> QuerySet[Notification]:
    notifications = get_notifications().filter(id__in=notification_ids)
    if len(notifications) != len(notification_ids):
        raise ValidationError("Some notifications do not exist")

    return notifications
