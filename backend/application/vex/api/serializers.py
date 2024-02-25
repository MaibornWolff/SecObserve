import validators
from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
)

from application.vex.models import (
    CSAF,
    CSAF_Revision,
    CSAF_Vulnerability,
    OpenVEX,
    OpenVEX_Vulnerability,
)
from application.vex.types import (
    CSAF_Publisher_Category,
    CSAF_TLP_Label,
    CSAF_Tracking_Status,
)


class CSAFDocumentCreateSerializer(Serializer):
    product_id = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_names = ListField(
        child=CharField(max_length=255), min_length=0, max_length=10, required=False
    )
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
    tlp_label = ChoiceField(
        choices=CSAF_TLP_Label.CSAF_TLP_LABEL_CHOICES, required=True
    )

    def validate_publisher_namespace(self, publisher_namespace: str) -> str:
        return _validate_url(publisher_namespace)


class CSAFDocumentUpdateSerializer(Serializer):
    publisher_name = CharField(max_length=255, required=False)
    publisher_category = ChoiceField(
        choices=CSAF_Publisher_Category.CSAF_PUBLISHER_CATEGORY_CHOICES, required=False
    )
    publisher_namespace = CharField(max_length=255, required=False)
    tracking_status = ChoiceField(
        choices=CSAF_Tracking_Status.CSAF_TRACKING_STATUS_CHOICES, required=False
    )

    def validate_publisher_namespace(self, publisher_namespace: str) -> str:
        return _validate_url(publisher_namespace)


class CSAFRevisionSerializer(ModelSerializer):
    class Meta:
        model = CSAF_Revision
        fields = ["date", "version", "summary"]


class CSAFVulnerabilitySerializer(ModelSerializer):
    class Meta:
        model = CSAF_Vulnerability
        fields = ["name"]


class CSAFSerializer(ModelSerializer):
    revisions = CSAFRevisionSerializer(many=True)
    vulnerability_names = CSAFVulnerabilitySerializer(many=True)

    class Meta:
        model = CSAF
        fields = "__all__"


class OpenVEXDocumentCreateSerializer(Serializer):
    product_id = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_names = ListField(
        child=CharField(max_length=255), min_length=0, max_length=10, required=False
    )
    document_id_prefix = CharField(max_length=200, required=True)
    author = CharField(max_length=255, required=True)
    role = CharField(max_length=255, required=False)

    def validate_document_id_prefix(self, document_id_prefix: str) -> str:
        return _validate_url(document_id_prefix)


class OpenVEXDocumentUpdateSerializer(Serializer):
    author = CharField(max_length=255, required=False)
    role = CharField(max_length=255, required=False)


class OpenVEXVulnerabilitySerializer(ModelSerializer):
    class Meta:
        model = OpenVEX_Vulnerability
        fields = ["name"]


class OpenVEXSerializer(ModelSerializer):
    vulnerability_names = OpenVEXVulnerabilitySerializer(many=True)

    class Meta:
        model = OpenVEX
        fields = "__all__"


def _validate_url(url: str) -> str:
    if url and not validators.url(url):
        raise ValidationError("Not a valid URL")

    return url
