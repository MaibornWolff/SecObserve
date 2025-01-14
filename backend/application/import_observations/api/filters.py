from django_filters import CharFilter, ChoiceFilter, FilterSet, OrderingFilter

from application.import_observations.models import (
    Api_Configuration,
    Parser,
    Vulnerability_Check,
)
from application.import_observations.types import Parser_Source, Parser_Type


class ApiConfigurationFilter(FilterSet):
    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("product", "product"),
            ("name", "name"),
            ("parser", "parser"),
        ),
    )

    class Meta:
        model = Api_Configuration
        fields = ["product", "name", "parser"]


class VulnerabilityCheckFilter(FilterSet):
    scanner = CharFilter(field_name="scanner", lookup_expr="icontains")
    filename = CharFilter(field_name="filename", lookup_expr="icontains")
    api_configuration_name = CharFilter(
        field_name="api_configuration_name", lookup_expr="icontains"
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("product", "product"),
            ("branch", "branch_name"),
            ("scanner", "scanner_name"),
            ("filename", "filename"),
            ("api_configuration_name", "api_configuration_name"),
            ("last_import", "last_import"),
            ("last_import_observations_new", "last_import_observations_new"),
            ("last_import_observations_updated", "last_import_observations_updated"),
            ("last_import_observations_resolved", "last_import_observations_resolved"),
        ),
    )

    class Meta:
        model = Vulnerability_Check
        fields = ["product", "branch", "scanner", "filename", "api_configuration_name"]


class ParserFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    type = ChoiceFilter(field_name="type", choices=Parser_Type.TYPE_CHOICES)
    source = ChoiceFilter(field_name="source", choices=Parser_Source.SOURCE_CHOICES)

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"), ("type", "type"), ("source", "source")),
    )

    class Meta:
        model = Parser
        fields = ["name", "type", "source"]
