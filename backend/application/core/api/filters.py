from datetime import timedelta

from django.utils import timezone
from django_filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    FilterSet,
    ModelChoiceFilter,
    OrderingFilter,
)

from application.commons.types import Age_Choices
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Observation_Log,
    Potential_Duplicate,
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
    Service,
)
from application.core.types import Status


class ProductGroupFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name")),
    )

    class Meta:
        model = Product
        fields = ["name", "license_policy"]


class ProductFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    age = ChoiceFilter(
        field_name="age", method="get_age", choices=Age_Choices.AGE_CHOICES
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("security_gate_passed", "security_gate_passed"),
            ("product_group__name", "product_group_name"),
            ("last_observation_change", "last_observation_change"),
        ),
    )

    def get_age(self, queryset, field_name, value):  # pylint: disable=unused-argument
        # field_name is used as a positional argument

        days = Age_Choices.get_days_from_age(value)

        if days is None:
            return queryset

        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_threshold = today - timedelta(days=int(days))
        return queryset.filter(last_observation_change__gte=time_threshold)

    class Meta:
        model = Product
        fields = ["name", "security_gate_passed", "product_group", "license_policy"]


class ProductMemberFilter(FilterSet):
    is_product_group = BooleanFilter(field_name="product__is_product_group")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("user__full_name", "user_data.full_name"),
            ("product__name", "product_data.name"),
            ("role", "role"),
        ),
    )

    class Meta:
        model = Product_Member
        fields = ["product", "user", "role"]


class ProductAuthorizationGroupMemberFilter(FilterSet):
    is_product_group = BooleanFilter(field_name="product__is_product_group")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("authorization_group__name", "authorization_group_data.name"),
            ("product__name", "product_data.name"),
            ("role", "role"),
        ),
    )

    class Meta:
        model = Product_Authorization_Group_Member
        fields = ["product", "authorization_group", "role"]


class BranchFilter(FilterSet):

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("last_import", "last_import"),
            ("purl", "purl"),
            ("cpe23", "cpe23"),
        ),
    )

    class Meta:
        model = Branch
        fields = ["product", "name"]


class ServiceFilter(FilterSet):
    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name")),
    )

    class Meta:
        model = Service
        fields = ["product", "name"]


class ObservationFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    origin_component_name_version = CharFilter(
        field_name="origin_component_name_version", lookup_expr="icontains"
    )
    origin_docker_image_name_tag_short = CharFilter(
        field_name="origin_docker_image_name_tag_short", lookup_expr="icontains"
    )
    origin_service_name = CharFilter(
        field_name="origin_service_name", lookup_expr="icontains"
    )
    origin_endpoint_hostname = CharFilter(
        field_name="origin_endpoint_hostname", lookup_expr="icontains"
    )
    origin_source_file = CharFilter(
        field_name="origin_source_file", lookup_expr="icontains"
    )
    origin_cloud_qualified_resource = CharFilter(
        field_name="origin_cloud_qualified_resource", lookup_expr="icontains"
    )
    origin_kubernetes_qualified_resource = CharFilter(
        field_name="origin_kubernetes_qualified_resource", lookup_expr="icontains"
    )
    scanner = CharFilter(field_name="scanner", lookup_expr="icontains")
    age = ChoiceFilter(
        field_name="age", method="get_age", choices=Age_Choices.AGE_CHOICES
    )
    product_group = ModelChoiceFilter(
        field_name="product__product_group",
        queryset=Product.objects.filter(is_product_group=True),
    )

    has_pending_assessment = BooleanFilter(
        field_name="has_pending_assessment",
        method="get_has_pending_assessment",
    )

    def get_has_pending_assessment(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        # field_name is used as a positional argument

        if value:
            return queryset.filter(
                id__in=Observation_Log.objects.filter(
                    assessment_status="Needs approval"
                ).values("observation_id")
            )

        return queryset.exclude(
            id__in=Observation_Log.objects.filter(
                assessment_status="Needs approval"
            ).values("observation_id")
        )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("id", "id"),
            ("product__name", "product_data.name"),
            ("product__product_group__name", "product_data.product_group_name"),
            ("branch__name", "branch_name"),
            ("title", "title"),
            ("numerical_severity", "current_severity"),
            ("current_status", "current_status"),
            ("origin_component_name_version", "origin_component_name_version"),
            (
                "origin_docker_image_name_tag_short",
                "origin_docker_image_name_tag_short",
            ),
            ("origin_service_name", "origin_service_name"),
            ("origin_endpoint_hostname", "origin_endpoint_hostname"),
            ("origin_source_file", "origin_source_file"),
            ("origin_cloud_qualified_resource", "origin_cloud_qualified_resource"),
            (
                "origin_kubernetes_qualified_resource",
                "origin_kubernetes_qualified_resource",
            ),
            ("parser__name", "parser_data.name"),
            ("parser__type", "parser_data.type"),
            ("scanner", "scanner_name"),
            ("last_observation_log", "last_observation_log"),
            ("epss_score", "epss_score"),
            ("has_potential_duplicates", "has_potential_duplicates"),
            ("origin_component_purl_type", "origin_component_purl_type"),
        ),
    )

    class Meta:  # pylint: disable=duplicate-code
        model = Observation
        fields = [
            "product",
            "branch",
            "title",
            "current_severity",
            "current_status",
            "parser",
            "scanner",
            "upload_filename",
            "api_configuration_name",
            "origin_service",
            "has_potential_duplicates",
            "origin_component_purl_type",
        ]

    def get_age(self, queryset, field_name, value):  # pylint: disable=unused-argument
        # field_name is used as a positional argument

        days = Age_Choices.get_days_from_age(value)

        if days is None:
            return queryset

        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_threshold = today - timedelta(days=int(days))
        return queryset.filter(last_observation_log__gte=time_threshold)


class ObservationLogFilter(FilterSet):
    age = ChoiceFilter(
        field_name="age", method="get_age", choices=Age_Choices.AGE_CHOICES
    )
    product = ModelChoiceFilter(
        field_name="observation__product",
        queryset=Product.objects.all(),
    )
    product_group = ModelChoiceFilter(
        field_name="observation__product__product_group",
        queryset=Product.objects.filter(is_product_group=True),
    )
    observation_title = CharFilter(
        field_name="observation__title",
        lookup_expr="icontains",
    )
    branch_name = CharFilter(
        field_name="observation__branch__name", lookup_expr="icontains"
    )
    branch = ModelChoiceFilter(
        field_name="observation__branch", queryset=Branch.objects.all()
    )
    origin_component_name_version = CharFilter(
        field_name="observation__origin_component_name_version", lookup_expr="icontains"
    )
    origin_docker_image_name_tag_short = CharFilter(
        field_name="observation__origin_docker_image_name_tag_short",
        lookup_expr="icontains",
    )
    origin_endpoint_hostname = CharFilter(
        field_name="observation__origin_endpoint_hostname", lookup_expr="icontains"
    )
    origin_source_file = CharFilter(
        field_name="observation__origin_source_file", lookup_expr="icontains"
    )
    origin_cloud_qualified_resource = CharFilter(
        field_name="observation__origin_cloud_qualified_resource",
        lookup_expr="icontains",
    )
    origin_kubernetes_qualified_resource = CharFilter(
        field_name="observation__origin_kubernetes_qualified_resource",
        lookup_expr="icontains",
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("id", "id"),
            ("user__full_name", "user_full_name"),
            ("observation__product__name", "observation_data.product_data.name"),
            (
                "observation__product__product_group__name",
                "observation_data.product_data.product_group_name",
            ),
            ("observation__branch__name", "observation_data.branch_name"),
            ("observation__title", "observation_data.title"),
            (
                "observation__origin_component_name_version",
                "observation_data.origin_component_name_version",
            ),
            (
                "observation__origin_docker_image_name_tag_short",
                "observation_data.origin_docker_image_name_tag_short",
            ),
            (
                "observation__origin_endpoint_hostname",
                "observation_data.origin_endpoint_hostname",
            ),
            ("observation__origin_source_file", "observation_data.origin_source_file"),
            (
                "observation__origin_cloud_qualified_resource",
                "observation_data.origin_cloud_qualified_resource",
            ),
            (
                "observation__origin_kubernetes_qualified_resource",
                "observation_data.origin_kubernetes_qualified_resource",
            ),
            ("severity", "severity"),
            ("status", "status"),
            ("comment", "comment"),
            ("created", "created"),
            ("assessment_status", "assessment_status"),
            ("approval_date", "approval_date"),
            ("approval_user__full_name", "approval_user_full_name"),
            ("vex_justification", "vex_justification"),
        ),
    )

    class Meta:
        model = Observation_Log
        fields = ["observation", "user", "assessment_status", "status", "severity"]

    def get_age(self, queryset, field_name, value):  # pylint: disable=unused-argument
        # field_name is used as a positional argument

        days = Age_Choices.get_days_from_age(value)

        if days is None:
            return queryset

        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_threshold = today - timedelta(days=int(days))
        return queryset.filter(created__gte=time_threshold)


class EvidenceFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"), ("observation", "observation")),
    )

    class Meta:
        model = Evidence
        fields = ["name", "observation"]


class PotentialDuplicateFilter(FilterSet):
    status = ChoiceFilter(
        field_name="potential_duplicate_observation__current_status",
        choices=Status.STATUS_CHOICES,
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            (
                "potential_duplicate_observation__title",
                "potential_duplicate_observation.title",
            ),
            (
                "potential_duplicate_observation__numerical_severity",
                "potential_duplicate_observation.current_severity",
            ),
            (
                "potential_duplicate_observation__current_status",
                "potential_duplicate_observation.current_status",
            ),
            (
                "potential_duplicate_observation__origin_service_name",
                "potential_duplicate_observation.origin_service_name",
            ),
            (
                "potential_duplicate_observation__origin_component_name_version",
                "potential_duplicate_observation.origin_component_name_version",
            ),
            (
                "potential_duplicate_observation__origin_docker_image_name_tag_short",
                "potential_duplicate_observation.origin_docker_image_name_tag_short",
            ),
            (
                "potential_duplicate_observation__origin_endpoint_hostname",
                "potential_duplicate_observation.origin_endpoint_hostname",
            ),
            (
                "potential_duplicate_observation__origin_source_file",
                "potential_duplicate_observation.origin_source_file",
            ),
            (
                "potential_duplicate_observation__origin_cloud_qualified_resource",
                "potential_duplicate_observation.origin_cloud_qualified_resource",
            ),
            (
                "potential_duplicate_observation__origin_kubernetes_qualified_resource",
                "potential_duplicate_observation__origin_kubernetes_qualified_resource",
            ),
            (
                "potential_duplicate_observation__scanner",
                "potential_duplicate_observation.scanner_name",
            ),
            (
                "potential_duplicate_observation__last_observation_log",
                "potential_duplicate_observation.last_observation_log",
            ),
        ),
    )

    class Meta:
        model = Potential_Duplicate
        fields = ["observation"]
