from django_filters import FilterSet, ModelChoiceFilter

from application.vex.models import CSAF, OpenVEX, CSAF_Vulnerability, OpenVEX_Vulnerability


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
