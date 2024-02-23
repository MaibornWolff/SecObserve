from django_filters import FilterSet

from application.vex.models import (
    CSAF,
    OpenVEX,
)


class CSAFFilter(FilterSet):
    # vulnerability_name = ModelChoiceFilter(queryset=CSAF_Vulnerability.objects.all())

    class Meta:
        model = CSAF
        fields = ["product"]


class OpenVEXFilter(FilterSet):
    # vulnerability_name = ModelChoiceFilter(queryset=OpenVEX_Vulnerability.objects.all())

    class Meta:
        model = OpenVEX
        fields = ["product"]
