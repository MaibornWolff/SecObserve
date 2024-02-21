from django.core.validators import MinValueValidator
from rest_framework.serializers import CharField, IntegerField, Serializer


class OpenVEXDocumentCreateSerializer(Serializer):
    product_id = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_name = CharField(max_length=255, required=False)
    document_id_prefix = CharField(max_length=200, required=True)
    author = CharField(max_length=255, required=True)


class OpenVEXDocumentUpdateSerializer(Serializer):
    document_id = CharField(max_length=255, required=True)
    author = CharField(max_length=255, required=False)
