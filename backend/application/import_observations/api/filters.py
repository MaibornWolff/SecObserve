from django_filters import FilterSet, OrderingFilter

from application.import_observations.models import (
    Api_Configuration,
    Vulnerability_Check,
)


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
