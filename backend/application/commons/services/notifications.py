from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from application.commons.models import Notification
from application.commons.services.global_request import get_current_user


def bulk_delete(notification_ids: list[int]) -> None:
    notifications = _check_notifications(notification_ids)
    notifications.delete()


def _check_notifications(notification_ids: list[int]) -> QuerySet[Notification]:
    notifications = Notification.objects.filter(id__in=notification_ids)
    if len(notifications) != len(notification_ids):
        raise ValidationError("Some notifications do not exist")

    user = get_current_user()
    if not user.is_superuser:
        for notification in notifications:
            if notification.user != user:
                raise ValidationError(
                    f"Notification {notification.pk} does not belong to user {user.full_name}"
                )

    return notifications
