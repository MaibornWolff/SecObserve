from typing import Optional

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
    SerializerMethodField,
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
    product = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_names = ListField(
        child=CharField(max_length=255), min_length=0, max_length=20, required=False
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
    tlp_label = ChoiceField(
        choices=CSAF_TLP_Label.CSAF_TLP_LABEL_CHOICES, required=True
    )
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
    product_name = SerializerMethodField()
    revisions = CSAFRevisionSerializer(many=True)
    vulnerability_names = SerializerMethodField()
    user_full_name = SerializerMethodField()

    class Meta:
        model = CSAF
        fields = "__all__"

    def get_product_name(self, obj: CSAF) -> Optional[str]:
        if obj.product:
            return obj.product.name
        return None

    def get_vulnerability_names(self, obj: CSAF) -> Optional[str]:
        vulnerabilities = [v.name for v in obj.vulnerability_names.all()]
        if vulnerabilities:
            return ", ".join(vulnerabilities)
        return None

    def get_user_full_name(self, obj: CSAF) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None


class OpenVEXDocumentCreateSerializer(Serializer):
    product = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_names = ListField(
        child=CharField(max_length=255), min_length=0, max_length=20, required=False
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
    product_name = SerializerMethodField()
    vulnerability_names = SerializerMethodField()
    user_full_name = SerializerMethodField()

    class Meta:
        model = OpenVEX
        fields = "__all__"

    def get_product_name(self, obj: OpenVEX) -> Optional[str]:
        if obj.product:
            return obj.product.name
        return None

    def get_vulnerability_names(self, obj: OpenVEX) -> Optional[str]:
        vulnerabilities = [v.name for v in obj.vulnerability_names.all()]
        if vulnerabilities:
            return ", ".join(vulnerabilities)
        return None

    def get_user_full_name(self, obj: OpenVEX) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None


def _validate_url(url: str) -> str:
    if url and not validators.url(url):
        raise ValidationError("Not a valid URL")

    return url
