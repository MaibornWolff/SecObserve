from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from application.access_control.services.current_user import get_current_user
from application.notifications.models import Notification, Notification_Viewed
from application.notifications.queries.notification import get_notifications


def bulk_mark_as_viewed(notification_ids: list[int]) -> None:
    notifications = _check_notifications(notification_ids)
    user = get_current_user()

    for notification in notifications:
        Notification_Viewed.objects.update_or_create(
            notification=notification,
            user=user,
        )


def _check_notifications(notification_ids: list[int]) -> QuerySet[Notification]:
    notifications = get_notifications().filter(id__in=notification_ids)
    if len(notifications) != len(notification_ids):
        raise ValidationError("Some notifications do not exist")

    if not get_current_user():
        raise ValidationError("No user in backend request")

    return notifications
