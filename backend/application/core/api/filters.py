from datetime import timedelta

from django.utils import timezone
from django_filters import (
    CharFilter,
    ChoiceFilter,
    FilterSet,
    ModelChoiceFilter,
    NumberFilter,
    OrderingFilter,
)

from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Parser,
    Product,
    Product_Member,
)

AGE_DAY = "Today"
AGE_WEEK = "Past 7 days"
AGE_MONTH = "Past 30 days"
AGE_QUARTER = "Past 90 days"
AGE_YEAR = "Past 365 days"

AGE_CHOICES = [
    (AGE_DAY, AGE_DAY),
    (AGE_WEEK, AGE_WEEK),
    (AGE_MONTH, AGE_MONTH),
    (AGE_QUARTER, AGE_QUARTER),
    (AGE_YEAR, AGE_YEAR),
]


class ProductGroupFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name")),
    )

    class Meta:
        model = Product
        fields = ["name"]


class ProductFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("security_gate_passed", "security_gate_passed"),
            ("product_group__name", "product_group_name"),
        ),
    )

    class Meta:
        model = Product
        fields = ["name", "security_gate_passed", "product_group"]


class ProductMemberFilter(FilterSet):
    product = NumberFilter(field_name="product")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("user__full_name", "user_data.full_name"),
            ("role", "role"),
        ),
    )

    class Meta:
        model = Product_Member
        fields = ["product", "user", "role"]


class BranchFilter(FilterSet):
    product = NumberFilter(field_name="product")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"), ("last_import", "last_import")),
    )

    class Meta:
        model = Branch
        fields = ["product", "name"]


class ParserFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    type = ChoiceFilter(field_name="type", choices=Parser.TYPE_CHOICES)
    source = ChoiceFilter(field_name="source", choices=Parser.SOURCE_CHOICES)

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"), ("type", "type"), ("source", "source")),
    )

    class Meta:
        model = Parser
        fields = ["name", "type", "source"]


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
    scanner = CharFilter(field_name="scanner", lookup_expr="icontains")
    age = ChoiceFilter(field_name="age", method="get_age", choices=AGE_CHOICES)
    product_group = ModelChoiceFilter(
        field_name="product__product_group",
        queryset=Product.objects.filter(is_product_group=True),
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
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
            ("parser__name", "parser_data.name"),
            ("parser__type", "parser_data.type"),
            ("scanner", "scanner_name"),
            ("last_observation_log", "last_observation_log"),
            ("epss_score", "epss_score"),
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
        ]

    def get_age(self, queryset, field_name, value):  # pylint: disable=unused-argument
        # field_name is used as a positional argument

        if value == AGE_DAY:
            days = 0
        elif value == AGE_WEEK:
            days = 7
        elif value == AGE_MONTH:
            days = 30
        elif value == AGE_QUARTER:
            days = 90
        elif value == AGE_YEAR:
            days = 365
        else:
            days = None

        if days is None:
            return queryset

        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_threshold = today - timedelta(days=int(days))
        return queryset.filter(last_observation_log__gte=time_threshold)


class EvidenceFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"), ("observation", "observation")),
    )

    class Meta:
        model = Evidence
        fields = ["name", "observation"]
