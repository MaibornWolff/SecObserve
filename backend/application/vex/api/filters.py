from django_filters import FilterSet, OrderingFilter

from application.vex.models import CSAF, OpenVEX


class CSAFFilter(FilterSet):
    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("vulnerability_name", "vulnerability_name"),
            ("product__name", "product"),
        )
    )

    class Meta:
        model = CSAF
        fields = ["vulnerability_name", "product"]


class OpenVEXFilter(FilterSet):
    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("vulnerability_name", "vulnerability_name"),
            ("product__name", "product"),
        )
    )

    class Meta:
        model = OpenVEX
        fields = ["vulnerability_name", "product"]
