from typing import Optional
from urllib.parse import urlparse

import validators
from django.utils import timezone
from packageurl import PackageURL
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)

from application.commons.services.global_request import get_current_user
from application.core.api.serializers_helpers import (
    get_branch_name,
    get_origin_component_name_version,
    get_scanner_name,
    validate_cvss3_vector,
    validate_cvss_and_severity,
)
from application.core.api.serializers_product import (
    NestedProductListSerializer,
    NestedProductSerializer,
)
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Observation_Log,
    Parser,
    Potential_Duplicate,
    Product,
    Reference,
)
from application.core.queries.observation import get_current_observation_log
from application.core.services.observation_log import create_observation_log
from application.core.services.security_gate import check_security_gate
from application.core.types import Assessment_Status, Severity, Status, VexJustification
from application.import_observations.types import Parser_Type
from application.issue_tracker.services.issue_tracker import (
    issue_tracker_factory,
    push_observation_to_issue_tracker,
)


class ParserSerializer(ModelSerializer):
    class Meta:
        model = Parser
        fields = "__all__"


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
    branch_name = SerializerMethodField()
    parser_data = ParserSerializer(source="parser")
    references = NestedReferenceSerializer(many=True)
    evidences = NestedEvidenceSerializer(many=True)
    origin_source_file_url = SerializerMethodField()
    origin_component_purl_type = SerializerMethodField()
    origin_component_purl_namespace = SerializerMethodField()
    issue_tracker_issue_url = SerializerMethodField()
    assessment_needs_approval = SerializerMethodField()

    class Meta:
        model = Observation
        exclude = ["numerical_severity", "issue_tracker_jira_initial_status"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["evidences"] = sorted(response["evidences"], key=lambda x: x["name"])
        return response

    def get_branch_name(self, observation: Observation) -> str:
        return get_branch_name(observation)

    def get_origin_source_file_url(self, observation: Observation) -> Optional[str]:
        origin_source_file_url = None

        if observation.product.repository_prefix and observation.origin_source_file:
            if not validators.url(observation.product.repository_prefix):
                return None

            parsed_url = urlparse(observation.product.repository_prefix)
            if parsed_url.scheme not in ["http", "https"]:
                return None

            origin_source_file_url = observation.product.repository_prefix
            if origin_source_file_url.endswith("/"):
                origin_source_file_url = origin_source_file_url[:-1]
            if parsed_url.netloc == "dev.azure.com":
                origin_source_file_url = self._create_azure_devops_url(
                    observation, origin_source_file_url
                )
            else:
                origin_source_file_url = self._create_common_url(
                    observation, origin_source_file_url
                )

        return origin_source_file_url

    def get_origin_component_purl_type(self, observation: Observation) -> str:
        if observation.origin_component_purl:
            purl = PackageURL.from_string(observation.origin_component_purl)
            return purl.type
        return ""

    def get_origin_component_purl_namespace(
        self, observation: Observation
    ) -> Optional[str]:
        if observation.origin_component_purl:
            purl = PackageURL.from_string(observation.origin_component_purl)
            return purl.namespace
        return ""

    def _create_azure_devops_url(
        self, observation: Observation, origin_source_file_url: str
    ) -> str:
        origin_source_file_url += f"?path={observation.origin_source_file}"
        if observation.branch:
            origin_source_file_url += f"&version=GB{observation.branch.name}"
        if observation.origin_source_line_start:
            origin_source_file_url += f"&line={observation.origin_source_line_start}"
            origin_source_file_url += "&lineStartColumn=1&lineEndColumn=1"
            if observation.origin_source_line_end:
                origin_source_file_url += (
                    f"&lineEnd={observation.origin_source_line_end+1}"
                )
            else:
                origin_source_file_url += (
                    f"&lineEnd={observation.origin_source_line_start+1}"
                )

        return origin_source_file_url

    def _create_common_url(
        self, observation: Observation, origin_source_file_url: str
    ) -> str:
        if observation.branch:
            origin_source_file_url += f"/{observation.branch.name}"
        origin_source_file_url += f"/{observation.origin_source_file}"
        if observation.origin_source_line_start:
            origin_source_file_url += "#L" + str(observation.origin_source_line_start)
        if observation.origin_source_line_end:
            origin_source_file_url += "-" + str(observation.origin_source_line_end)

        return origin_source_file_url

    def get_issue_tracker_issue_url(self, observation: Observation) -> Optional[str]:
        issue_url = None

        if observation.issue_tracker_issue_id:
            issue_tracker = issue_tracker_factory(
                observation.product, with_communication=False
            )
            issue_url = issue_tracker.get_frontend_issue_url(
                observation.product, observation.issue_tracker_issue_id
            )

        return issue_url

    def get_assessment_needs_approval(self, observation: Observation) -> Optional[int]:
        current_observation_log = get_current_observation_log(observation)
        if (
            current_observation_log
            and current_observation_log.assessment_status
            == Assessment_Status.ASSESSMENT_STATUS_NEEDS_APPROVAL
        ):
            return current_observation_log.pk
        return None

    def validate_product(self, product: Product) -> Product:
        if product and product.is_product_group:
            raise ValidationError("Product must not be a product group")

        return product


class ObservationListSerializer(ModelSerializer):
    product_data = NestedProductListSerializer(source="product")
    branch_name = SerializerMethodField()
    parser_data = ParserSerializer(source="parser")
    scanner_name = SerializerMethodField()
    origin_component_name_version = SerializerMethodField()

    class Meta:
        model = Observation
        exclude = ["numerical_severity", "issue_tracker_jira_initial_status"]

    def get_branch_name(self, observation: Observation) -> str:
        return get_branch_name(observation)

    def get_scanner_name(self, observation: Observation) -> str:
        return get_scanner_name(observation)

    def get_origin_component_name_version(self, observation: Observation) -> str:
        return get_origin_component_name_version(observation)


class ObservationUpdateSerializer(ModelSerializer):
    def validate(self, attrs: dict):
        self.instance: Observation
        if self.instance and self.instance.parser.type != Parser_Type.TYPE_MANUAL:
            raise ValidationError("Only manual observations can be updated")

        attrs["import_last_seen"] = timezone.now()

        validate_cvss_and_severity(attrs)

        return super().validate(attrs)

    def validate_branch(self, branch: Branch) -> Branch:
        if branch and branch.product != self.instance.product:
            raise ValidationError(
                "Branch does not belong to the same product as the observation"
            )

        return branch

    def validate_cvss3_vector(self, cvss3_vector: str) -> str:
        return validate_cvss3_vector(cvss3_vector)

    def update(self, instance: Observation, validated_data: dict):
        actual_severity = instance.current_severity
        actual_status = instance.current_status
        actual_vex_justification = instance.current_vex_justification

        instance.origin_component_name = ""
        instance.origin_component_version = ""

        instance.origin_docker_image_name = ""
        instance.origin_docker_image_tag = ""
        instance.origin_docker_image_digest = ""

        observation: Observation = super().update(instance, validated_data)

        if actual_severity != observation.current_severity:
            actual_severity = observation.current_severity
        else:
            actual_severity = ""

        if actual_status != observation.current_status:
            actual_status = observation.current_status
        else:
            actual_status = ""

        if actual_vex_justification != observation.current_vex_justification:
            actual_vex_justification = observation.current_vex_justification
        else:
            actual_vex_justification = ""

        if actual_severity or actual_status:
            create_observation_log(
                observation,
                actual_severity,
                actual_status,
                "Observation changed manually",
                actual_vex_justification,
                Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
            )

        check_security_gate(observation.product)
        push_observation_to_issue_tracker(observation, get_current_user())
        if observation.branch:
            observation.branch.last_import = timezone.now()
            observation.branch.save()

        return observation

    def to_representation(self, instance):
        serializer = ObservationSerializer(instance)
        return serializer.data

    class Meta:
        model = Observation
        fields = [
            "branch",
            "title",
            "description",
            "recommendation",
            "parser_severity",
            "parser_status",
            "parser_vex_justification",
            "origin_component_name_version",
            "origin_component_name",
            "origin_component_version",
            "origin_docker_image_name_tag",
            "origin_docker_image_name",
            "origin_docker_image_tag",
            "origin_endpoint_url",
            "origin_service_name",
            "origin_source_file",
            "origin_source_line_start",
            "origin_source_line_end",
            "origin_cloud_provider",
            "origin_cloud_account_subscription_project",
            "origin_cloud_resource",
            "origin_cloud_resource_type",
            "vulnerability_id",
            "cvss3_score",
            "cvss3_vector",
            "cwe",
        ]


class ObservationCreateSerializer(ModelSerializer):
    def validate(self, attrs):
        attrs["parser"] = Parser.objects.get(type=Parser_Type.TYPE_MANUAL)
        attrs["scanner"] = Parser_Type.TYPE_MANUAL
        attrs["import_last_seen"] = timezone.now()

        if attrs.get("branch"):
            if attrs["branch"].product != attrs["product"]:
                raise ValidationError(
                    "Branch does not belong to the same product as the observation"
                )

        validate_cvss_and_severity(attrs)

        return super().validate(attrs)

    def validate_cvss3_vector(self, cvss3_vector: str) -> str:
        return validate_cvss3_vector(cvss3_vector)

    def create(self, validated_data):
        observation: Observation = super().create(validated_data)

        create_observation_log(
            observation,
            observation.current_severity,
            observation.current_status,
            "Observation created manually",
            observation.current_vex_justification,
            Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
        )

        check_security_gate(observation.product)
        push_observation_to_issue_tracker(observation, get_current_user())
        if observation.branch:
            observation.branch.last_import = timezone.now()
            observation.branch.save()

        return observation

    def to_representation(self, instance):
        serializer = ObservationSerializer(instance)
        return serializer.data

    class Meta:
        model = Observation
        fields = [
            "product",
            "branch",
            "title",
            "description",
            "recommendation",
            "parser_severity",
            "parser_status",
            "parser_vex_justification",
            "origin_component_name_version",
            "origin_component_name",
            "origin_component_version",
            "origin_docker_image_name_tag",
            "origin_docker_image_name",
            "origin_docker_image_tag",
            "origin_endpoint_url",
            "origin_service_name",
            "origin_source_file",
            "origin_source_line_start",
            "origin_source_line_end",
            "origin_cloud_provider",
            "origin_cloud_account_subscription_project",
            "origin_cloud_resource",
            "origin_cloud_resource_type",
            "vulnerability_id",
            "cvss3_score",
            "cvss3_vector",
            "cwe",
        ]


class ObservationAssessmentSerializer(Serializer):
    severity = ChoiceField(choices=Severity.SEVERITY_CHOICES, required=False)
    status = ChoiceField(choices=Status.STATUS_CHOICES, required=False)
    vex_justification = ChoiceField(
        choices=VexJustification.VEX_JUSTIFICATION_CHOICES,
        required=False,
        allow_blank=True,
    )
    comment = CharField(max_length=255, required=True)


class ObservationRemoveAssessmentSerializer(Serializer):
    comment = CharField(max_length=255, required=True)


class ObservationBulkDeleteSerializer(Serializer):
    observations = ListField(
        child=IntegerField(min_value=1), min_length=0, max_length=100, required=True
    )


class ObservationBulkAssessmentSerializer(Serializer):
    severity = ChoiceField(choices=Severity.SEVERITY_CHOICES, required=False)
    status = ChoiceField(choices=Status.STATUS_CHOICES, required=False)
    comment = CharField(max_length=255, required=True)
    observations = ListField(
        child=IntegerField(min_value=1), min_length=0, max_length=100, required=True
    )
    vex_justification = ChoiceField(
        choices=VexJustification.VEX_JUSTIFICATION_CHOICES,
        required=False,
        allow_blank=True,
    )


class ObservationBulkMarkDuplicatesSerializer(Serializer):
    observation_id = IntegerField(min_value=1, required=True)
    potential_duplicates = ListField(
        child=IntegerField(min_value=1), min_length=0, max_length=100, required=True
    )


class NestedObservationSerializer(ModelSerializer):
    scanner_name = SerializerMethodField()
    origin_component_name_version = SerializerMethodField()

    class Meta:
        model = Observation
        exclude = ["numerical_severity", "issue_tracker_jira_initial_status"]

    def get_scanner_name(self, observation: Observation) -> str:
        return get_scanner_name(observation)

    def get_origin_component_name_version(self, observation: Observation) -> str:
        return get_origin_component_name_version(observation)


class ObservationLogSerializer(ModelSerializer):
    observation_data = ObservationSerializer(source="observation")
    user_full_name = SerializerMethodField()
    approval_user_full_name = SerializerMethodField()

    def get_user_full_name(self, obj: Observation_Log) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None

    def get_approval_user_full_name(self, obj: Observation_Log) -> Optional[str]:
        if obj.approval_user:
            return obj.approval_user.full_name

        return None

    class Meta:
        model = Observation_Log
        fields = "__all__"


class ObservationLogListSerializer(ModelSerializer):
    observation_title = SerializerMethodField()
    user_full_name = SerializerMethodField()
    approval_user_full_name = SerializerMethodField()

    def get_user_full_name(self, obj: Observation_Log) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None

    def get_observation_title(self, obj: Observation_Log) -> str:
        return obj.observation.title

    def get_approval_user_full_name(self, obj: Observation_Log) -> Optional[str]:
        if obj.approval_user:
            return obj.approval_user.full_name

        return None

    class Meta:
        model = Observation_Log
        fields = "__all__"


class ObservationLogApprovalSerializer(Serializer):
    assessment_status = ChoiceField(
        choices=Assessment_Status.ASSESSMENT_STATUS_CHOICES_APPROVAL, required=False
    )
    approval_remark = CharField(max_length=255, required=True)


class PotentialDuplicateSerializer(ModelSerializer):
    potential_duplicate_observation = NestedObservationSerializer()

    class Meta:
        model = Potential_Duplicate
        fields = "__all__"
