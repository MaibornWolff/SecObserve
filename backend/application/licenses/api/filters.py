from django_filters import BooleanFilter, CharFilter, FilterSet, OrderingFilter

from application.commons.api.extended_ordering_filter import ExtendedOrderingFilter
from application.licenses.models import (
    License,
    License_Component,
    License_Group,
    License_Group_Member,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)


class LicenseComponentFilter(FilterSet):
    name_version = CharFilter(field_name="name_version", lookup_expr="icontains")
    license_spdx_id = CharFilter(field_name="license__spdx_id", lookup_expr="icontains")
    unknown_license = CharFilter(field_name="unknown_license", lookup_expr="icontains")

    ordering = ExtendedOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("license__spdx_id", "license_data.spdx_id"),
            ("unknown_license", "unknown_license"),
            (
                (
                    "numerical_evaluation_result",
                    "license__spdx_id",
                    "unknown_license",
                    "name_version",
                ),
                "evaluation_result",
            ),
            ("branch__name", "branch_name"),
            ("name_version", "name_version"),
            ("purl_type", "purl_type"),
        ),
    )

    class Meta:
        model = License_Component
        fields = [
            "product",
            "branch",
            "license_spdx_id",
            "unknown_license",
            "evaluation_result",
            "name_version",
            "purl_type",
        ]


class LicenseFilter(FilterSet):
    spdx_id = CharFilter(field_name="spdx_id", lookup_expr="icontains")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    is_in_license_group = BooleanFilter(
        field_name="is_in_license_group", method="get_is_in_license_group"
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("spdx_id", "spdx_id"),
            ("name", "name"),
            ("is_osi_approved", "is_osi_approved"),
            ("is_deprecated", "is_deprecated"),
        ),
    )

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="spdx_id", lookup_expr="icontains")

    class Meta:
        model = License
        fields = [
            "spdx_id",
            "name",
            "is_osi_approved",
            "is_deprecated",
            "license_groups",
        ]

    def get_is_in_license_group(
        self, queryset, field_name, value  # pylint: disable=unused-argument
    ) -> bool:
        return queryset.filter(license_groups__isnull=not value)


class LicenseGroupFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("is_public", "is_public"),
        ),
    )

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = License_Group
        fields = ["name", "is_public", "licenses"]


class LicenseGroupMemberFilter(FilterSet):
    username = CharFilter(field_name="user__username", lookup_expr="icontains")
    full_name = CharFilter(field_name="user__full_name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("user__full_name", "user_data.full_name"),
            ("license_group", "license_group"),
            ("user", "user"),
        ),
    )

    class Meta:
        model = License_Group_Member
        fields = ["license_group", "user", "username", "full_name"]


class LicensePolicyFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("is_public", "is_public"),
        ),
    )

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = License_Policy
        fields = ["name", "is_public"]


class LicensePolicyItemFilter(FilterSet):
    license_group_name = CharFilter(
        field_name="license_group__name", lookup_expr="icontains"
    )
    license_spdx_id = CharFilter(field_name="license__spdx_id", lookup_expr="icontains")
    unknown_license = CharFilter(field_name="unknown_license", lookup_expr="icontains")

    ordering = ExtendedOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("license_policy__name", "license_policy_data.name"),
            (
                ("license_group__name", "license__spdx_id", "unknown_license"),
                "license_group_name",
            ),
            (
                ("license__spdx_id", "license_group__name", "unknown_license"),
                "license_spdx_id",
            ),
            (
                ("unknown_license", "license_group__name", "license__spdx_id"),
                "unknown_license",
            ),
            (
                (
                    "numerical_evaluation_result",
                    "license_group__name",
                    "license__spdx_id",
                    "unknown_license",
                ),
                "evaluation_result",
            ),
        ),
    )

    class Meta:
        model = License_Policy_Item
        fields = [
            "license_policy",
            "license_group_name",
            "license_spdx_id",
            "unknown_license",
            "evaluation_result",
            "license_group_name",
        ]


class LicensePolicyMemberFilter(FilterSet):
    username = CharFilter(field_name="user__username", lookup_expr="icontains")
    full_name = CharFilter(field_name="user__full_name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("user__full_name", "user_data.full_name"),
            ("license_policy", "license_policy"),
            ("user", "user"),
        ),
    )

    class Meta:
        model = License_Policy_Member
        fields = ["license_policy", "user", "username", "full_name"]
