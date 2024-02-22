from django.core.validators import MinValueValidator
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from application.vex.models import OpenVEX


class OpenVEXDocumentCreateSerializer(Serializer):
    product_id = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_name = CharField(max_length=255, required=False)
    document_id_prefix = CharField(max_length=200, required=True)
    author = CharField(max_length=255, required=True)
    role = CharField(max_length=255, required=False)


class OpenVEXDocumentUpdateSerializer(Serializer):
    author = CharField(max_length=255, required=False)
    role = CharField(max_length=255, required=False)


class OpenVEXSerializer(ModelSerializer):
    class Meta:
        model = OpenVEX
        fields = "__all__"
