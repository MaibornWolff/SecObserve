from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from application.access_control.services.authorization import user_has_permission
from application.access_control.services.roles_permissions import Permissions
from application.commons.models import Notification
from application.commons.queries.notification import get_notifications
from application.commons.services.global_request import get_current_user


def bulk_delete(notification_ids: list[int]) -> None:
    notifications = _check_notifications(notification_ids)
    notifications.delete()


def _check_notifications(notification_ids: list[int]) -> QuerySet[Notification]:
    notifications = get_notifications().filter(id__in=notification_ids)
    if len(notifications) != len(notification_ids):
        raise ValidationError("Some notifications do not exist")

    user = get_current_user()
    if not user:
        raise ValidationError("No user in backend request")

    if not user.is_superuser:
        for notification in notifications:
            if not notification.product or not user_has_permission(
                notification.product, Permissions.Product_Delete
            ):
                raise ValidationError(
                    "User does not have permission to delete some notifications"
                )

    return notifications
