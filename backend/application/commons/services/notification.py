from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from application.commons.models import Notification, Notification_Viewed
from application.commons.queries.notification import get_notifications
from application.commons.services.global_request import get_current_user


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
