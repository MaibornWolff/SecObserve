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
    name = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    message = TextField(max_length=4096)
    user = ForeignKey(User, on_delete=CASCADE, null=True)
    product = ForeignKey(Product, on_delete=CASCADE, null=True)
    observation = ForeignKey(Observation, on_delete=CASCADE, null=True)
    function = CharField(max_length=255, blank=True)
    arguments = TextField(max_length=4096, blank=True)
