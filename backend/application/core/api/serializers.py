from decimal import Decimal
import re
from typing import Optional
from urllib.parse import urlparse

import validators
from cvss import CVSS3, CVSSError
from django.utils import timezone
from packageurl import PackageURL
from rest_framework.exceptions import PermissionDenied
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

from application.access_control.api.serializers import UserSerializer
from application.access_control.services.roles_permissions import (
    Permissions,
    Roles,
    get_permissions_for_role,
)
from application.commons.services.global_request import get_current_user
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Observation_Log,
    Parser,
    Potential_Duplicate,
    Product,
    Product_Member,
    Reference,
    Service,
)
from application.core.queries.product_member import get_product_member
from application.core.services.observation import get_cvss3_severity
from application.core.services.observation_log import create_observation_log
from application.core.services.security_gate import check_security_gate
from application.core.types import Severity, Status, VexJustification
from application.import_observations.types import Parser_Type
from application.issue_tracker.services.issue_tracker import (
    issue_tracker_factory,
    push_observation_to_issue_tracker,
)
from application.issue_tracker.types import Issue_Tracker


class ProductCoreSerializer(ModelSerializer):
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

        return []

    def validate(self, attrs: dict):
        if attrs.get("repository_branch_housekeeping_active"):
            if not attrs.get("repository_branch_housekeeping_keep_inactive_days"):
                attrs["repository_branch_housekeeping_keep_inactive_days"] = 1
        else:
            attrs["repository_branch_housekeeping_keep_inactive_days"] = None
            attrs["repository_branch_housekeeping_exempt_branches"] = ""

        if attrs.get("security_gate_active"):
            if not attrs.get("security_gate_threshold_critical"):
                attrs["security_gate_threshold_critical"] = 0
            if not attrs.get("security_gate_threshold_high"):
                attrs["security_gate_threshold_high"] = 0
            if not attrs.get("security_gate_threshold_medium"):
                attrs["security_gate_threshold_medium"] = 0
            if not attrs.get("security_gate_threshold_low"):
                attrs["security_gate_threshold_low"] = 0
            if not attrs.get("security_gate_threshold_none"):
                attrs["security_gate_threshold_none"] = 0
            if not attrs.get("security_gate_threshold_unkown"):
                attrs["security_gate_threshold_unkown"] = 0
        else:
            attrs["security_gate_threshold_critical"] = None
            attrs["security_gate_threshold_high"] = None
            attrs["security_gate_threshold_medium"] = None
            attrs["security_gate_threshold_low"] = None
            attrs["security_gate_threshold_none"] = None
            attrs["security_gate_threshold_unkown"] = None

        return super().validate(attrs)


class ProductGroupSerializer(ProductCoreSerializer):
    products_count = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "products_count",
            "permissions",
            "open_critical_observation_count",
            "open_high_observation_count",
            "open_medium_observation_count",
            "open_low_observation_count",
            "open_none_observation_count",
            "open_unkown_observation_count",
            "repository_branch_housekeeping_active",
            "repository_branch_housekeeping_keep_inactive_days",
            "repository_branch_housekeeping_exempt_branches",
            "notification_ms_teams_webhook",
            "notification_slack_webhook",
            "notification_email_to",
            "security_gate_active",
            "security_gate_threshold_critical",
            "security_gate_threshold_high",
            "security_gate_threshold_medium",
            "security_gate_threshold_low",
            "security_gate_threshold_none",
            "security_gate_threshold_unkown",
        ]

    def get_products_count(self, obj: Product) -> int:
        return obj.products.count()

    def create(self, validated_data: dict) -> Product:
        product_group = super().create(validated_data)
        product_group.is_product_group = True
        product_group.save()
        return product_group

    def update(self, instance: Product, validated_data: dict) -> Product:
        product_group = super().update(instance, validated_data)
        if product_group.is_product_group is False:
            product_group.is_product_group = True
            product_group.save()
        return product_group


class ProductSerializer(ProductCoreSerializer):
    product_group_name = SerializerMethodField()
    product_group_repository_branch_housekeeping_active = SerializerMethodField()
    product_group_security_gate_active = SerializerMethodField()
    repository_default_branch_name = SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["is_product_group"]

    def get_product_group_name(self, obj: Product) -> str:
        if not obj.product_group:
            return ""
        return obj.product_group.name

    def get_product_group_repository_branch_housekeeping_active(
        self, obj: Product
    ) -> Optional[bool]:
        if not obj.product_group:
            return None
        return obj.product_group.repository_branch_housekeeping_active

    def get_product_group_security_gate_active(self, obj: Product) -> Optional[bool]:
        if not obj.product_group:
            return None
        return obj.product_group.security_gate_active

    def get_repository_default_branch_name(self, obj: Product) -> str:
        if not obj.repository_default_branch:
            return ""
        return obj.repository_default_branch.name

    def validate(self, attrs: dict):  # pylint: disable=too-many-branches
        # There are quite a lot of branches, but at least they are not nested too much
        if attrs.get("issue_tracker_type") == Issue_Tracker.ISSUE_TRACKER_GITHUB:
            attrs["issue_tracker_base_url"] = "https://api.github.com"

        if not (
            attrs.get("issue_tracker_type")
            and attrs.get("issue_tracker_base_url")
            and attrs.get("issue_tracker_api_key")
            and attrs.get("issue_tracker_project_id")
        ) and not (
            not attrs.get("issue_tracker_type")
            and not attrs.get("issue_tracker_base_url")
            and not attrs.get("issue_tracker_api_key")
            and not attrs.get("issue_tracker_project_id")
        ):
            raise ValidationError(
                "Either all or none of the issue tracker fields must be set"
            )

        if attrs.get("issue_tracker_active") and not attrs.get("issue_tracker_type"):
            raise ValidationError(
                "Issue tracker data must be set when issue tracking is active"
            )

        if attrs.get("issue_tracker_type") == Issue_Tracker.ISSUE_TRACKER_JIRA:
            if not attrs.get("issue_tracker_username"):
                raise ValidationError(
                    "Username must be set when issue tracker type is Jira"
                )
            if not attrs.get("issue_tracker_issue_type"):
                raise ValidationError(
                    "Issue type must be set when issue tracker type is Jira"
                )
            if not attrs.get("issue_tracker_status_closed"):
                raise ValidationError(
                    "Closed status must be set when issue tracker type is Jira"
                )

        if (
            attrs.get("issue_tracker_type")
            and attrs.get("issue_tracker_type") != Issue_Tracker.ISSUE_TRACKER_JIRA
        ):
            if attrs.get("issue_tracker_username"):
                raise ValidationError(
                    "Username must not be set when issue tracker type is not Jira"
                )
            if attrs.get("issue_tracker_issue_type"):
                raise ValidationError(
                    "Isse type must not be set when issue tracker type is not Jira"
                )
            if attrs.get("issue_tracker_status_closed"):
                raise ValidationError(
                    "Closed status must not be set when issue tracker type is not Jira"
                )

        return super().validate(attrs)

    def validate_product_group(self, product: Product) -> Product:
        if product and product.is_product_group is False:
            raise ValidationError("Product group must be a product group")

        return product

    def validate_repository_prefix(self, repository_prefix: str) -> str:
        return _validate_url(repository_prefix)

    def validate_notification_ms_teams_webhook(self, repository_prefix: str) -> str:
        return _validate_url(repository_prefix)

    def validate_notification_slack_webhook(self, repository_prefix: str) -> str:
        return _validate_url(repository_prefix)

    def validate_purl(self, purl: str) -> str:
        if purl:
            try:
                PackageURL.from_string(purl)
            except ValueError as e:
                raise ValidationError(str(e))

        return purl

    def validate_cpe23(self, cpe23: str) -> str:
        if cpe23:
            # Regex taken from https://csrc.nist.gov/schema/cpe/2.3/cpe-naming_2.3.xsd
            if not re.match(
                r"""cpe:2\.3:[aho\*\-](:(((\?*|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){5}(:(([a-zA-Z]{2,3}(-([a-zA-Z]{2}|[0-9]{3}))?)|[\*\-]))(:(((\?*|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){4}""",  # noqa: E501
                cpe23,
            ):
                raise ValidationError("Not a valid CPE 2.3")
        return cpe23


class NestedProductSerializer(ModelSerializer):
    permissions = SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["is_product_group"]

    def get_permissions(self, product: Product) -> list[Permissions]:
        user = get_current_user()
        if user and user.is_superuser:
            return get_permissions_for_role(Roles.Owner)

        product_member = get_product_member(product)
        if product_member:
            return get_permissions_for_role(product_member.role)

        return []


class NestedProductListSerializer(ModelSerializer):
    product_group_name = SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["members", "is_product_group"]

    def get_product_group_name(self, obj: Product) -> str:
        if not obj.product_group:
            return ""
        return obj.product_group.name


class ProductMemberSerializer(ModelSerializer):
    user_data = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Product_Member
        fields = "__all__"

    def validate(self, attrs: dict):
        self.instance: Product_Member
        data_product: Optional[Product] = attrs.get("product")
        data_user = attrs.get("user")

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
        if attrs.get("role") == Roles.Owner and (
            not current_user
            or not own_product_member
            or (
                not current_user.is_superuser and own_product_member.role != Roles.Owner
            )
        ):
            raise PermissionDenied("You are not permitted to add a member as Owner")

        return attrs


class BranchSerializer(ModelSerializer):
    name_with_product = SerializerMethodField()
    is_default_branch = SerializerMethodField()
    open_critical_observation_count = SerializerMethodField()
    open_high_observation_count = SerializerMethodField()
    open_medium_observation_count = SerializerMethodField()
    open_low_observation_count = SerializerMethodField()
    open_none_observation_count = SerializerMethodField()
    open_unkown_observation_count = SerializerMethodField()

    class Meta:
        model = Branch
        fields = "__all__"

    def get_name_with_product(self, obj: Service) -> str:
        return f"{obj.name} ({obj.product.name})"

    def get_is_default_branch(self, obj: Branch) -> bool:
        return obj.product.repository_default_branch == obj

    def get_open_critical_observation_count(self, obj: Branch) -> int:
        return obj.open_critical_observation_count

    def get_open_high_observation_count(self, obj: Branch) -> int:
        return obj.open_high_observation_count

    def get_open_medium_observation_count(self, obj: Branch) -> int:
        return obj.open_medium_observation_count

    def get_open_low_observation_count(self, obj: Branch) -> int:
        return obj.open_low_observation_count

    def get_open_none_observation_count(self, obj: Branch) -> int:
        return obj.open_none_observation_count

    def get_open_unkown_observation_count(self, obj: Branch) -> int:
        return obj.open_unkown_observation_count


class ServiceSerializer(ModelSerializer):
    name_with_product = SerializerMethodField()
    open_critical_observation_count = SerializerMethodField()
    open_high_observation_count = SerializerMethodField()
    open_medium_observation_count = SerializerMethodField()
    open_low_observation_count = SerializerMethodField()
    open_none_observation_count = SerializerMethodField()
    open_unkown_observation_count = SerializerMethodField()

    class Meta:
        model = Service
        fields = "__all__"

    def get_name_with_product(self, obj: Service) -> str:
        return f"{obj.name} ({obj.product.name})"

    def get_open_critical_observation_count(self, obj: Service) -> int:
        return obj.open_critical_observation_count

    def get_open_high_observation_count(self, obj: Service) -> int:
        return obj.open_high_observation_count

    def get_open_medium_observation_count(self, obj: Service) -> int:
        return obj.open_medium_observation_count

    def get_open_low_observation_count(self, obj: Service) -> int:
        return obj.open_low_observation_count

    def get_open_none_observation_count(self, obj: Service) -> int:
        return obj.open_none_observation_count

    def get_open_unkown_observation_count(self, obj: Service) -> int:
        return obj.open_unkown_observation_count


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
    branch_name = SerializerMethodField()
    parser_data = ParserSerializer(source="parser")
    observation_logs = NestedObservationLogSerializer(many=True)
    references = NestedReferenceSerializer(many=True)
    evidences = NestedEvidenceSerializer(many=True)
    origin_source_file_url = SerializerMethodField()
    origin_component_purl_type = SerializerMethodField()
    issue_tracker_issue_url = SerializerMethodField()

    class Meta:
        model = Observation
        exclude = ["numerical_severity", "issue_tracker_jira_initial_status"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["evidences"] = sorted(response["evidences"], key=lambda x: x["name"])
        return response

    def get_branch_name(self, observation: Observation) -> str:
        return _get_branch_name(observation)

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
        return _get_branch_name(observation)

    def get_scanner_name(self, observation: Observation) -> str:
        return _get_scanner_name(observation)

    def get_origin_component_name_version(self, observation: Observation) -> str:
        return _get_origin_component_name_version(observation)


class ObservationUpdateSerializer(ModelSerializer):
    def validate(self, attrs: dict):
        self.instance: Observation
        if self.instance and self.instance.parser.type != Parser_Type.TYPE_MANUAL:
            raise ValidationError("Only manual observations can be updated")

        attrs["import_last_seen"] = timezone.now()

        _validate_cvss_and_severity(attrs)

        return super().validate(attrs)

    def validate_branch(self, branch: Branch) -> Branch:
        if branch and branch.product != self.instance.product:
            raise ValidationError(
                "Branch does not belong to the same product as the observation"
            )

        return branch

    def validate_cvss3_vector(self, cvss3_vector: str) -> str:
        return _validate_cvss3_vector(cvss3_vector)

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

        _validate_cvss_and_severity(attrs)

        return super().validate(attrs)

    def validate_cvss3_vector(self, cvss3_vector: str) -> str:
        return _validate_cvss3_vector(cvss3_vector)

    def create(self, validated_data):
        observation: Observation = super().create(validated_data)

        create_observation_log(
            observation,
            observation.current_severity,
            observation.current_status,
            "Observation created manually",
            observation.current_vex_justification,
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
        return _get_scanner_name(observation)

    def get_origin_component_name_version(self, observation: Observation) -> str:
        return _get_origin_component_name_version(observation)


class PotentialDuplicateSerializer(ModelSerializer):
    potential_duplicate_observation = NestedObservationSerializer()

    class Meta:
        model = Potential_Duplicate
        fields = "__all__"


def _get_branch_name(observation: Observation) -> str:
    if not observation.branch:
        return ""

    return observation.branch.name


def _get_scanner_name(observation: Observation) -> str:
    if not observation.scanner:
        return ""

    scanner_parts = observation.scanner.split("/")
    return scanner_parts[0].strip()


def _get_origin_component_name_version(observation: Observation) -> str:
    if not observation.origin_component_name:
        return ""

    origin_component_name_version_with_type = observation.origin_component_name_version
    if observation.origin_component_purl:
        purl = PackageURL.from_string(observation.origin_component_purl)
        if purl.type:
            origin_component_name_version_with_type += f" ({purl.type})"

    return origin_component_name_version_with_type


def _validate_url(url: str) -> str:
    if url and not validators.url(url):
        raise ValidationError("Not a valid URL")

    return url


def _validate_cvss3_vector(cvss3_vector):
    if cvss3_vector:
        try:
            cvss3 = CVSS3(cvss3_vector)
            cvss3_vector = cvss3.clean_vector()
        except CVSSError as e:
            raise ValidationError(str(e))  # pylint: disable=raise-missing-from
        # The CVSSError itself is not relevant and must not be re-raised

    return cvss3_vector


def _validate_cvss_and_severity(attrs):
    base_score = None
    if attrs.get("cvss3_vector"):
        cvss3 = CVSS3(attrs.get("cvss3_vector"))
        base_score = Decimal(cvss3.scores()[0]).quantize(Decimal(".0"))

    cvss3_score = attrs.get("cvss3_score")
    if cvss3_score is not None:
        if base_score is not None and base_score != cvss3_score:
            raise ValidationError(
                f"Score from CVSS3 vector ({base_score}) is different than CVSS3 score ({cvss3_score})"
            )
    else:
        attrs["cvss3_score"] = base_score

    cvss3_score = attrs.get("cvss3_score")
    cvss3_severity = (
        get_cvss3_severity(cvss3_score) if cvss3_score is not None else None
    )
    parser_severity = attrs.get("parser_severity")

    if parser_severity:
        if parser_severity != cvss3_severity:
            raise ValidationError(
                f"Severity ({parser_severity}) is different than severity from CVSS3 score ({cvss3_severity})"
            )
    else:
        if not cvss3_severity:
            raise ValidationError(
                "Either Severity, CVSS3 score or CVSS3 vector has to be set"
            )
