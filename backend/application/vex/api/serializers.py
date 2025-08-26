from typing import Optional

import validators
from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    FileField,
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from application.core.api.serializers_product import NestedProductSerializer
from application.vex.models import (
    CSAF,
    CSAF_Branch,
    CSAF_Revision,
    CSAF_Vulnerability,
    CycloneDX,
    CycloneDX_Branch,
    CycloneDX_Vulnerability,
    OpenVEX,
    OpenVEX_Branch,
    OpenVEX_Vulnerability,
    VEX_Counter,
    VEX_Document,
    VEX_Statement,
)
from application.vex.types import (
    CSAF_Publisher_Category,
    CSAF_TLP_Label,
    CSAF_Tracking_Status,
)


class CSAFDocumentCreateSerializer(Serializer):
    product = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_names = ListField(child=CharField(max_length=255), min_length=0, max_length=20, required=False)
    branch_names = ListField(child=CharField(max_length=255), min_length=0, max_length=20, required=False)
    branches = ListField(child=IntegerField(min_value=1), min_length=0, max_length=20, required=False)
    document_id_prefix = CharField(max_length=200, required=True)
    title = CharField(max_length=255, required=True)
    publisher_name = CharField(max_length=255, required=True)
    publisher_category = ChoiceField(choices=CSAF_Publisher_Category.CSAF_PUBLISHER_CATEGORY_CHOICES, required=True)
    publisher_namespace = CharField(max_length=255, required=True)
    tracking_status = ChoiceField(choices=CSAF_Tracking_Status.CSAF_TRACKING_STATUS_CHOICES, required=True)
    tlp_label = ChoiceField(choices=CSAF_TLP_Label.CSAF_TLP_LABEL_CHOICES, required=True)

    def validate_publisher_namespace(self, publisher_namespace: str) -> str:
        return _validate_url(publisher_namespace)


class CSAFDocumentUpdateSerializer(Serializer):
    tlp_label = ChoiceField(choices=CSAF_TLP_Label.CSAF_TLP_LABEL_CHOICES, required=True)
    publisher_name = CharField(max_length=255, required=False)
    publisher_category = ChoiceField(choices=CSAF_Publisher_Category.CSAF_PUBLISHER_CATEGORY_CHOICES, required=False)
    publisher_namespace = CharField(max_length=255, required=False)
    tracking_status = ChoiceField(choices=CSAF_Tracking_Status.CSAF_TRACKING_STATUS_CHOICES, required=False)

    def validate_publisher_namespace(self, publisher_namespace: str) -> str:
        return _validate_url(publisher_namespace)


class CSAFRevisionSerializer(ModelSerializer):
    class Meta:
        model = CSAF_Revision
        fields = ["date", "version", "summary"]


class CSAFSerializer(ModelSerializer):
    product_data = NestedProductSerializer(source="product")
    revisions = CSAFRevisionSerializer(many=True)
    vulnerability_names = SerializerMethodField()
    branch_names = SerializerMethodField()
    user_full_name = SerializerMethodField()

    class Meta:
        model = CSAF
        fields = "__all__"

    def get_vulnerability_names(self, obj: CSAF) -> Optional[str]:
        vulnerabilities = [v.name for v in obj.vulnerability_names.all()]
        if vulnerabilities:
            return ", ".join(vulnerabilities)
        return None

    def get_branch_names(self, obj: CSAF) -> Optional[str]:
        branches = [b.branch.name for b in obj.branches.all()]
        if branches:
            return ", ".join(branches)
        return None

    def get_user_full_name(self, obj: CSAF) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None


class CSAFVulnerabilitySerializer(ModelSerializer):
    class Meta:
        model = CSAF_Vulnerability
        fields = "__all__"


class CSAFBranchSerializer(ModelSerializer):
    name = SerializerMethodField(read_only=True)

    class Meta:
        model = CSAF_Branch
        fields = "__all__"

    def get_name(self, obj: CSAF_Branch) -> str:
        return obj.branch.name


class OpenVEXDocumentCreateSerializer(Serializer):
    product = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_names = ListField(child=CharField(max_length=255), min_length=0, max_length=20, required=False)
    branch_names = ListField(child=CharField(max_length=255), min_length=0, max_length=20, required=False)
    branches = ListField(child=IntegerField(min_value=1), min_length=0, max_length=20, required=False)
    id_namespace = CharField(max_length=255, required=True)
    document_id_prefix = CharField(max_length=255, required=True)
    author = CharField(max_length=255, required=True)
    role = CharField(max_length=255, required=False)

    def validate_id_namespace(self, id_namespace: str) -> str:
        return _validate_url(id_namespace)


class OpenVEXDocumentUpdateSerializer(Serializer):
    author = CharField(max_length=255, required=False)
    role = CharField(max_length=255, required=False)


class OpenVEXSerializer(ModelSerializer):
    product_data = NestedProductSerializer(source="product")
    vulnerability_names = SerializerMethodField()
    branch_names = SerializerMethodField()
    user_full_name = SerializerMethodField()

    class Meta:
        model = OpenVEX
        fields = "__all__"

    def get_vulnerability_names(self, obj: OpenVEX) -> Optional[str]:
        vulnerabilities = [v.name for v in obj.vulnerability_names.all()]
        if vulnerabilities:
            return ", ".join(vulnerabilities)
        return None

    def get_branch_names(self, obj: OpenVEX) -> Optional[str]:
        branches = [b.branch.name for b in obj.branches.all()]
        if branches:
            return ", ".join(branches)
        return None

    def get_user_full_name(self, obj: OpenVEX) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None


class OpenVEXVulnerabilitySerializer(ModelSerializer):
    class Meta:
        model = OpenVEX_Vulnerability
        fields = "__all__"


class OpenVEXBranchSerializer(ModelSerializer):
    name = SerializerMethodField(read_only=True)

    class Meta:
        model = OpenVEX_Branch
        fields = "__all__"

    def get_name(self, obj: OpenVEX_Branch) -> str:
        return obj.branch.name


class CycloneDXDocumentCreateSerializer(Serializer):
    product = IntegerField(validators=[MinValueValidator(0)], required=False)
    vulnerability_names = ListField(child=CharField(max_length=255), min_length=0, max_length=20, required=False)
    branches = ListField(child=IntegerField(min_value=1), min_length=0, max_length=20, required=False)
    document_id_prefix = CharField(max_length=255, required=False)
    author = CharField(max_length=255, required=False, allow_blank=True)
    manufacturer = CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs: dict) -> dict:
        if not attrs.get("author") and not attrs.get("manufacturer"):
            raise ValidationError("Either author or manufacturer must be set")
        if attrs.get("author") and attrs.get("manufacturer"):
            raise ValidationError("Only one of author or manufacturer must be set")

        return super().validate(attrs)


class CycloneDXDocumentUpdateSerializer(Serializer):
    author = CharField(max_length=255, required=False, allow_blank=True)
    manufacturer = CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs: dict) -> dict:
        if not attrs.get("author") and not attrs.get("manufacturer"):
            raise ValidationError("Either author or manufacturer must be set")
        if attrs.get("author") and attrs.get("manufacturer"):
            raise ValidationError("Only one of author or manufacturer must be set")

        return super().validate(attrs)


class CycloneDXSerializer(ModelSerializer):
    product_data = NestedProductSerializer(source="product")
    vulnerability_names = SerializerMethodField()
    branch_names = SerializerMethodField()
    user_full_name = SerializerMethodField()

    class Meta:
        model = CycloneDX
        fields = "__all__"

    def get_vulnerability_names(self, obj: CycloneDX) -> Optional[str]:
        vulnerabilities = [v.name for v in obj.vulnerability_names.all()]
        if vulnerabilities:
            return ", ".join(vulnerabilities)
        return None

    def get_branch_names(self, obj: CycloneDX) -> Optional[str]:
        branches = [b.branch.name for b in obj.branches.all()]
        if branches:
            return ", ".join(branches)
        return None

    def get_user_full_name(self, obj: CycloneDX) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None


class CycloneDXVulnerabilitySerializer(ModelSerializer):
    class Meta:
        model = CycloneDX_Vulnerability
        fields = "__all__"


class CycloneDXBranchSerializer(ModelSerializer):
    name = SerializerMethodField(read_only=True)

    class Meta:
        model = CycloneDX_Branch
        fields = "__all__"

    def get_name(self, obj: OpenVEX_Branch) -> str:
        return obj.branch.name


class VEXCounterSerializer(ModelSerializer):
    class Meta:
        model = VEX_Counter
        fields = "__all__"


class VEXDocumentSerializer(ModelSerializer):
    class Meta:
        model = VEX_Document
        fields = "__all__"


class VEXStatementSerializer(ModelSerializer):
    class Meta:
        model = VEX_Statement
        fields = "__all__"


class VEXImportSerializer(Serializer):
    file = FileField(max_length=255)


def _validate_url(url: str) -> str:
    if url and not validators.url(url):
        raise ValidationError("Not a valid URL")

    return url
