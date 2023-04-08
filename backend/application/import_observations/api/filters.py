from django_filters import FilterSet, OrderingFilter

from application.import_observations.models import Api_Configuration


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
