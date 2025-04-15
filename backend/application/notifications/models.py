from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)

from application.access_control.models import User
from application.core.models import Observation, Product


class Notification(Model):
    TYPE_EXCEPTION = "Exception"
    TYPE_SECURITY_GATE = "Security gate"
    TYPE_TASK = "Task"

    TYPE_CHOICES = [
        (TYPE_EXCEPTION, TYPE_EXCEPTION),
        (TYPE_SECURITY_GATE, TYPE_SECURITY_GATE),
        (TYPE_TASK, TYPE_TASK),
    ]

    name = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    message = TextField(max_length=4096)
    user = ForeignKey(User, on_delete=CASCADE, null=True)
    product = ForeignKey(Product, on_delete=CASCADE, null=True)
    observation = ForeignKey(Observation, on_delete=CASCADE, null=True)
    type = CharField(max_length=20, choices=TYPE_CHOICES)
    function = CharField(max_length=255, blank=True)
    arguments = TextField(max_length=4096, blank=True)

    class Meta:
        db_table = "commons_notification"


class Notification_Viewed(Model):
    notification = ForeignKey(Notification, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        db_table = "commons_notification_viewed"
