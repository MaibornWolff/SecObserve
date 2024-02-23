import validators
from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from application.vex.models import CSAF, OpenVEX
from application.vex.types import CSAF_Publisher_Category, CSAF_Tracking_Status


class CSAFDocumentCreateSerializer(Serializer):
    product_id = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_name = CharField(max_length=255, required=False)
    document_id_prefix = CharField(max_length=200, required=True)
    title = CharField(max_length=255, required=True)
    publisher_name = CharField(max_length=255, required=True)
    publisher_category = ChoiceField(
        choices=CSAF_Publisher_Category.CSAF_PUBLISHER_CATEGORY_CHOICES, required=True
    )
    publisher_namespace = CharField(max_length=255, required=True)
    tracking_status = ChoiceField(
        choices=CSAF_Tracking_Status.CSAF_TRACKING_STATUS_CHOICES, required=True
    )

    def validate_publisher_namespace(self, publisher_namespace: str) -> str:
        return _validate_url(publisher_namespace)


class CSAFSerializer(ModelSerializer):
    class Meta:
        model = CSAF
        fields = "__all__"


class OpenVEXDocumentCreateSerializer(Serializer):
    product_id = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_name = CharField(max_length=255, required=False)
    document_id_prefix = CharField(max_length=200, required=True)
    author = CharField(max_length=255, required=True)
    role = CharField(max_length=255, required=False)

    def validate_document_id_prefix(self, document_id_prefix: str) -> str:
        return _validate_url(document_id_prefix)


class OpenVEXDocumentUpdateSerializer(Serializer):
    author = CharField(max_length=255, required=False)
    role = CharField(max_length=255, required=False)


class OpenVEXSerializer(ModelSerializer):
    class Meta:
        model = OpenVEX
        fields = "__all__"


def _validate_url(url: str) -> str:
    if url and not validators.url(url):
        raise ValidationError("Not a valid URL")

    return url
