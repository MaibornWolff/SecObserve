from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    CASCADE,
    PROTECT,
)
from encrypted_model_fields.fields import EncryptedCharField

from application.core.models import Product, Parser


class Api_Configuration(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    name = CharField(max_length=255)
    parser = ForeignKey(Parser, on_delete=PROTECT)
    base_url = CharField(max_length=255)
    project_key = CharField(max_length=255)
    api_key = EncryptedCharField(max_length=255)

    class Meta:
        unique_together = (
            "product",
            "name",
        )
