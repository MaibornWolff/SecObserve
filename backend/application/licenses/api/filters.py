from django_filters import CharFilter, FilterSet, OrderingFilter, BooleanFilter

from application.licenses.models import License, License_Group


class LicenseFilter(FilterSet):
    license_id = CharFilter(field_name="license_id", lookup_expr="icontains")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    is_in_license_group = BooleanFilter(field_name="is_in_license_group", method="get_is_in_license_group")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("license_id", "license_id"),
            ("name", "name"),
            ("is_osi_approved", "is_osi_approved"),
            ("is_deprecated", "is_deprecated"),
        ),
    )

    class Meta:
        model = License
        fields = ["license_id", "name", "is_osi_approved", "is_deprecated", "license_groups"]

    def get_is_in_license_group(self, queryset, field_name, value) -> bool:
        return queryset.filter(license_groups__isnull=not value)

class LicenseGroupFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"),),
    )

    class Meta:
        model = License_Group
        fields = ["name", "licenses"]
