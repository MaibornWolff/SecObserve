from datetime import datetime
from typing import Optional

from django.utils.timezone import make_aware
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)

from application.access_control.api.serializers import UserSerializer
from application.access_control.services.roles_permissions import (
    Permissions,
    Roles,
    get_permissions_for_role,
)
from application.commons.services.global_request import get_current_user
from application.core.models import (
    Evidence,
    Observation,
    Observation_Log,
    Parser,
    Product,
    Product_Member,
    Reference,
)
from application.core.queries.product import get_product_member
from application.core.services.observation_log import create_observation_log


class ProductSerializer(ModelSerializer):
    open_critical_observation_count = SerializerMethodField()
    open_high_observation_count = SerializerMethodField()
    open_medium_observation_count = SerializerMethodField()
    open_low_observation_count = SerializerMethodField()
    open_none_observation_count = SerializerMethodField()
    open_unkown_observation_count = SerializerMethodField()
    permissions = SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_open_critical_observation_count(self, obj: Product) -> int:
        return obj.open_critical_observation_count

    def get_open_high_observation_count(self, obj: Product) -> int:
        return obj.open_high_observation_count

    def get_open_medium_observation_count(self, obj: Product) -> int:
        return obj.open_medium_observation_count

    def get_open_low_observation_count(self, obj: Product) -> int:
        return obj.open_low_observation_count

    def get_open_none_observation_count(self, obj: Product) -> int:
        return obj.open_none_observation_count

    def get_open_unkown_observation_count(self, obj: Product) -> int:
        return obj.open_unkown_observation_count

    def get_permissions(self, obj: Product) -> list[Permissions]:
        user = get_current_user()
        if user and user.is_superuser:
            return get_permissions_for_role(Roles.Owner)

        product_member = get_product_member(obj)
        if product_member:
            return get_permissions_for_role(product_member.role)
        else:
            return []

    def validate(self, data: dict):
        if data.get("security_gate_active"):
            if not data.get("security_gate_threshold_critical"):
                data["security_gate_threshold_critical"] = 0
            if not data.get("security_gate_threshold_high"):
                data["security_gate_threshold_high"] = 0
            if not data.get("security_gate_threshold_medium"):
                data["security_gate_threshold_medium"] = 0
            if not data.get("security_gate_threshold_low"):
                data["security_gate_threshold_low"] = 0
            if not data.get("security_gate_threshold_none"):
                data["security_gate_threshold_none"] = 0
            if not data.get("security_gate_threshold_unkown"):
                data["security_gate_threshold_unkown"] = 0
        else:
            data["security_gate_threshold_critical"] = None
            data["security_gate_threshold_high"] = None
            data["security_gate_threshold_medium"] = None
            data["security_gate_threshold_low"] = None
            data["security_gate_threshold_none"] = None
            data["security_gate_threshold_unkown"] = None
        return super().validate(data)


class NestedProductSerializer(ModelSerializer):
    permissions = SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_permissions(self, product: Product) -> list[Permissions]:
        user = get_current_user()
        if user and user.is_superuser:
            return get_permissions_for_role(Roles.Owner)

        product_member = get_product_member(product)
        if product_member:
            return get_permissions_for_role(product_member.role)
        else:
            return []


class NestedProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ["members"]


class ProductMemberSerializer(ModelSerializer):
    user_data = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Product_Member
        fields = "__all__"

    def validate(self, data: dict):
        self.instance: Product_Member
        data_product: Optional[Product] = data.get("product")
        data_user = data.get("user")

        if self.instance is not None and (
            (data_product and data_product != self.instance.product)
            or (data_user and data_user != self.instance.user)
        ):
            raise ValidationError("Product and user cannot be changed")

        if self.instance is None:
            product_member = get_product_member(data_product, data_user)
            if product_member:
                raise ValidationError(f"Product member {data_user} already exists")

        if self.instance is not None:
            own_product_member = get_product_member(
                self.instance.product, get_current_user()
            )
        else:
            own_product_member = get_product_member(data_product, get_current_user())

        current_user = get_current_user()
        if data.get("role") == Roles.Owner and (
            not current_user
            or not own_product_member
            or (
                not current_user.is_superuser and own_product_member.role != Roles.Owner
            )
        ):
            raise PermissionDenied("You are not permitted to add a member as Owner")

        return data


class ParserSerializer(ModelSerializer):
    class Meta:
        model = Parser
        fields = "__all__"


class NestedObservationLogSerializer(ModelSerializer):
    class Meta:
        model = Observation_Log
        exclude = ["observation"]


class NestedReferenceSerializer(ModelSerializer):
    class Meta:
        model = Reference
        exclude = ["observation"]


class NestedEvidenceSerializer(ModelSerializer):
    class Meta:
        model = Evidence
        exclude = ["observation", "evidence"]


class EvidenceSerializer(ModelSerializer):
    product = SerializerMethodField()

    class Meta:
        model = Evidence
        fields = "__all__"

    def get_product(self, evidence: Evidence) -> int:
        return evidence.observation.product.pk


class ObservationSerializer(ModelSerializer):
    product_data = NestedProductSerializer(source="product")
    parser_data = ParserSerializer(source="parser")
    observation_logs = NestedObservationLogSerializer(many=True)
    references = NestedReferenceSerializer(many=True)
    evidences = NestedEvidenceSerializer(many=True)
    origin_source_file_url = SerializerMethodField()

    class Meta:
        model = Observation
        exclude = ["numerical_severity"]

    def get_origin_source_file_url(self, observation: Observation) -> Optional[str]:
        origin_source_file_url = None

        if observation.product.repository_prefix and observation.origin_source_file:
            origin_source_file_url = observation.product.repository_prefix
            if not origin_source_file_url.endswith("/"):
                origin_source_file_url += "/"
            origin_source_file_url += observation.origin_source_file
            if observation.origin_source_line_start:
                origin_source_file_url += "#L" + str(
                    observation.origin_source_line_start
                )
            if observation.origin_source_line_end:
                origin_source_file_url += "-" + str(observation.origin_source_line_end)

        return origin_source_file_url


class ObservationListSerializer(ModelSerializer):
    product_data = NestedProductListSerializer(source="product")
    parser_data = ParserSerializer(source="parser")
    scanner_name = SerializerMethodField()

    class Meta:
        model = Observation
        exclude = ["numerical_severity"]

    def get_scanner_name(self, observation: Observation) -> str:
        if observation.scanner:
            scanner_parts = observation.scanner.split("/")
            return scanner_parts[0].strip()
        else:
            return ""


class ObservationUpdateSerializer(ModelSerializer):
    def validate(self, data: dict):
        self.instance: Observation
        if self.instance and self.instance.parser.type != Parser.TYPE_MANUAL:
            raise ValidationError("Only manual observations can be updated")

        data["import_last_seen"] = make_aware(datetime.now())
        return super().validate(data)

    def update(self, instance: Observation, validated_data: dict):
        actual_severity = instance.current_severity
        actual_status = instance.current_status

        instance.origin_component_name = ""
        instance.origin_component_version = ""

        instance.origin_docker_image_name = ""
        instance.origin_docker_image_tag = ""

        observation: Observation = super().update(instance, validated_data)

        if actual_severity != observation.current_severity:
            actual_severity = observation.current_severity
        else:
            actual_severity = ""

        if actual_status != observation.current_status:
            actual_status = observation.current_status
        else:
            actual_status = ""

        if actual_severity or actual_status:
            create_observation_log(
                observation,
                actual_severity,
                actual_status,
                "Observation changed manually",
            )
        return observation

    def to_representation(self, instance):
        serializer = ObservationSerializer(instance)
        return serializer.data

    class Meta:
        model = Observation
        fields = [
            "title",
            "description",
            "recommendation",
            "current_severity",
            "current_status",
            "origin_component_name_version",
            "origin_docker_image_name_tag",
            "origin_endpoint_url",
            "origin_service_name",
            "origin_source_file",
            "origin_source_line_start",
            "origin_source_line_end",
        ]


class ObservationCreateSerializer(ModelSerializer):
    def validate(self, data):
        manual_parser = Parser.objects.get(type=Parser.TYPE_MANUAL)
        data["parser"] = manual_parser
        data["scanner"] = Parser.TYPE_MANUAL
        data["import_last_seen"] = make_aware(datetime.now())
        return super().validate(data)

    def create(self, validated_data):
        observation: Observation = super().create(validated_data)
        create_observation_log(
            observation,
            observation.current_severity,
            observation.current_status,
            "Observation created manually",
        )
        return observation

    def to_representation(self, instance):
        serializer = ObservationSerializer(instance)
        return serializer.data

    class Meta:
        model = Observation
        fields = [
            "product",
            "title",
            "description",
            "recommendation",
            "current_severity",
            "current_status",
            "origin_component_name_version",
            "origin_docker_image_name_tag",
            "origin_endpoint_url",
            "origin_service_name",
            "origin_source_file",
            "origin_source_line_start",
            "origin_source_line_end",
        ]


class ObservationAssessmentSerializer(Serializer):
    severity = ChoiceField(choices=Observation.SEVERITY_CHOICES, required=False)
    status = ChoiceField(choices=Observation.STATUS_CHOICES, required=False)
    comment = CharField(max_length=255, required=True)


class ObservationRemoveAssessmentSerializer(Serializer):
    comment = CharField(max_length=255, required=True)
