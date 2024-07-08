from datetime import date
from typing import Optional

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from application.access_control.api.serializers import UserListSerializer
from application.access_control.services.authorization import get_highest_user_role
from application.access_control.services.roles_permissions import (
    Permissions,
    Roles,
    get_permissions_for_role,
)
from application.commons.services.global_request import get_current_user
from application.core.api.serializers_helpers import (
    validate_cpe23,
    validate_purl,
    validate_url,
)
from application.core.models import (
    Branch,
    Observation,
    Observation_Log,
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
    Service,
)
from application.core.queries.product_member import (
    get_product_authorization_group_member,
    get_product_member,
)
from application.core.services.risk_acceptance_expiry import (
    calculate_risk_acceptance_expiry_date,
)
from application.core.types import Assessment_Status, Status
from application.issue_tracker.types import Issue_Tracker
from application.rules.models import Rule
from application.rules.types import Rule_Status


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
        return get_permissions_for_role(get_highest_user_role(obj))

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
            "assessments_need_approval",
            "product_rules_need_approval",
            "risk_acceptance_expiry_active",
            "risk_acceptance_expiry_days",
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
    product_group_assessments_need_approval = SerializerMethodField()
    repository_default_branch_name = SerializerMethodField()
    observation_reviews = SerializerMethodField()
    observation_log_approvals = SerializerMethodField()
    has_services = SerializerMethodField()
    product_group_product_rules_need_approval = SerializerMethodField()
    product_rule_approvals = SerializerMethodField()
    risk_acceptance_expiry_date_calculated = SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["is_product_group", "new_observations_in_review", "members"]

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

    def get_product_group_assessments_need_approval(self, obj: Product) -> bool:
        if not obj.product_group:
            return False
        return obj.product_group.assessments_need_approval

    def get_repository_default_branch_name(self, obj: Product) -> str:
        if not obj.repository_default_branch:
            return ""
        return obj.repository_default_branch.name

    def get_observation_reviews(self, obj: Product) -> int:
        return Observation.objects.filter(
            product=obj, current_status=Status.STATUS_IN_REVIEW
        ).count()

    def get_observation_log_approvals(self, obj: Product) -> int:
        if obj.product_group:
            if (
                not obj.product_group.assessments_need_approval
                and not obj.assessments_need_approval
            ):
                return 0
        else:
            if not obj.assessments_need_approval:
                return 0

        return Observation_Log.objects.filter(
            observation__product=obj,
            assessment_status=Assessment_Status.ASSESSMENT_STATUS_NEEDS_APPROVAL,
        ).count()

    def get_has_services(self, obj: Product) -> bool:
        return Service.objects.filter(product=obj).exists()

    def get_product_group_product_rules_need_approval(self, obj: Product) -> bool:
        if not obj.product_group:
            return False
        return obj.product_group.product_rules_need_approval

    def get_product_rule_approvals(self, obj: Product) -> int:
        if obj.product_group:
            if (
                not obj.product_group.product_rules_need_approval
                and not obj.product_rules_need_approval
            ):
                return 0
        else:
            if not obj.product_rules_need_approval:
                return 0

        return Rule.objects.filter(
            product=obj, approval_status=Rule_Status.RULE_STATUS_NEEDS_APPROVAL
        ).count()

    def get_risk_acceptance_expiry_date_calculated(
        self, obj: Product
    ) -> Optional[date]:
        return calculate_risk_acceptance_expiry_date(obj)

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
        return validate_url(repository_prefix)

    def validate_notification_ms_teams_webhook(self, repository_prefix: str) -> str:
        return validate_url(repository_prefix)

    def validate_notification_slack_webhook(self, repository_prefix: str) -> str:
        return validate_url(repository_prefix)

    def validate_purl(self, purl: str) -> str:
        return validate_purl(purl)

    def validate_cpe23(self, cpe23: str) -> str:
        return validate_cpe23(cpe23)


class NestedProductSerializer(ModelSerializer):
    permissions = SerializerMethodField()
    product_group_assessments_need_approval = SerializerMethodField()
    product_group_product_rules_need_approval = SerializerMethodField()
    risk_acceptance_expiry_date_calculated = SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["is_product_group", "new_observations_in_review", "members"]

    def get_permissions(self, product: Product) -> list[Permissions]:
        return get_permissions_for_role(get_highest_user_role(product))

    def get_product_group_assessments_need_approval(self, obj: Product) -> bool:
        if not obj.product_group:
            return False
        return obj.product_group.assessments_need_approval

    def get_product_group_product_rules_need_approval(self, obj: Product) -> bool:
        if not obj.product_group:
            return False
        return obj.product_group.product_rules_need_approval

    def get_risk_acceptance_expiry_date_calculated(
        self, obj: Product
    ) -> Optional[date]:
        return calculate_risk_acceptance_expiry_date(obj)


class NestedProductListSerializer(ModelSerializer):
    product_group_name = SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["members", "is_product_group", "new_observations_in_review"]

    def get_product_group_name(self, obj: Product) -> str:
        if not obj.product_group:
            return ""
        return obj.product_group.name


class ProductMemberSerializer(ModelSerializer):
    user_data = UserListSerializer(source="user", read_only=True)

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

        current_user = get_current_user()
        if self.instance is not None:
            role = get_highest_user_role(self.instance.product, current_user)
        else:
            role = get_highest_user_role(data_product, current_user)

        if (
            attrs.get("role")  # pylint: disable=too-many-boolean-expressions
            != Roles.Owner
            or (current_user and current_user.is_superuser)
            or role == Roles.Owner
        ):
            # if statement is still structured and readable
            pass
        else:
            raise ValidationError("You are not permitted to add a member as Owner")

        return attrs


class ProductAuthorizationGroupMemberSerializer(ModelSerializer):
    authorization_group_name = SerializerMethodField()

    class Meta:
        model = Product_Authorization_Group_Member
        fields = "__all__"

    def get_authorization_group_name(
        self, obj: Product_Authorization_Group_Member
    ) -> str:
        return obj.authorization_group.name

    def validate(self, attrs: dict):
        self.instance: Product_Authorization_Group_Member
        data_product: Optional[Product] = attrs.get("product")
        data_authorization_group = attrs.get("authorization_group")

        if self.instance is not None and (
            (data_product and data_product != self.instance.product)
            or (
                data_authorization_group
                and data_authorization_group != self.instance.authorization_group
            )
        ):
            raise ValidationError("Product and authorization group cannot be changed")

        if self.instance is None:
            product_authorization_group_member = get_product_authorization_group_member(
                data_product, data_authorization_group
            )
            if product_authorization_group_member:
                raise ValidationError(
                    f"Product member {data_authorization_group} already exists"
                )

        current_user = get_current_user()
        if self.instance is not None:
            role = get_highest_user_role(self.instance.product, current_user)
        else:
            role = get_highest_user_role(data_product, current_user)

        if (
            attrs.get("role")  # pylint: disable=too-many-boolean-expressions
            != Roles.Owner
            or (current_user and current_user.is_superuser)
            or role == Roles.Owner
        ):
            # if statement is still structured and readable
            pass
        else:
            raise ValidationError("You are not permitted to add a member as Owner")

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

    def validate_purl(self, purl: str) -> str:
        return validate_purl(purl)

    def validate_cpe23(self, cpe23: str) -> str:
        return validate_cpe23(cpe23)

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
