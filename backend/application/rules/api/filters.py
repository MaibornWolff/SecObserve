from django_filters import CharFilter, FilterSet, OrderingFilter

from application.rules.models import Rule


class GeneralRuleFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("parser", "parser"),
            ("scanner_prefix", "scanner_prefix"),
            ("title", "title"),
            ("new_severity", "new_severity"),
            ("new_status", "new_status"),
            ("enabled", "enabled"),
            ("approval_status", "approval_status"),
        ),
    )

    class Meta:
        model = Rule
        fields = [
            "name",
            "search",
            "parser",
            "scanner_prefix",
            "title",
            "enabled",
            "approval_status",
        ]


class ProductRuleFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("product", "product"),
            ("parser", "parser"),
            ("scanner_prefix", "scanner_prefix"),
            ("title", "title"),
            ("new_severity", "new_severity"),
            ("new_status", "new_status"),
            ("enabled", "enabled"),
            ("approval_status", "approval_status"),
        ),
    )

    class Meta:
        model = Rule
        fields = [
            "name",
            "search",
            "product",
            "parser",
            "scanner_prefix",
            "title",
            "enabled",
            "approval_status",
        ]
