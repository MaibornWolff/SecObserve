from datetime import timedelta

from django.utils import timezone
from django_filters import (
    CharFilter,
    ChoiceFilter,
    FilterSet,
    NumberFilter,
    OrderingFilter,
)

from application.commons.api.extended_ordering_filter import ExtendedOrderingFilter
from application.commons.types import Age_Choices
from application.licenses.models import (
    License,
    License_Component,
    License_Group,
    License_Group_Authorization_Group_Member,
    License_Group_Member,
    License_Policy,
    License_Policy_Authorization_Group_Member,
    License_Policy_Item,
    License_Policy_Member,
)


class LicenseComponentFilter(FilterSet):
    name_version = CharFilter(field_name="name_version", lookup_expr="icontains")
    license_spdx_id = CharFilter(field_name="license__spdx_id", lookup_expr="icontains")
    unknown_license = CharFilter(field_name="unknown_license", lookup_expr="icontains")
    age = ChoiceFilter(
        field_name="age", method="get_age", choices=Age_Choices.AGE_CHOICES
    )

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
            ("last_change", "last_change"),
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

    def get_age(self, queryset, field_name, value):  # pylint: disable=unused-argument
        # field_name is used as a positional argument

        days = Age_Choices.get_days_from_age(value)

        if days is None:
            return queryset

        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_threshold = today - timedelta(days=int(days))
        return queryset.filter(last_change__gte=time_threshold)


class LicenseFilter(FilterSet):
    spdx_id = CharFilter(field_name="spdx_id", lookup_expr="icontains")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    exclude_license_group = NumberFilter(
        field_name="exclude_license_group", method="get_exclude_license_group"
    )
    exclude_license_policy = NumberFilter(
        field_name="exclude_license_policy", method="get_exclude_license_policy"
    )

    def get_exclude_license_group(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        if value is not None:
            return queryset.exclude(license_groups__id=value)
        return queryset

    def get_exclude_license_policy(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        if value is not None:
            return queryset.exclude(license_policy_items__license_policy__id=value)
        return queryset

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("spdx_id", "spdx_id"),
            ("name", "name"),
            ("is_osi_approved", "is_osi_approved"),
            ("is_deprecated", "is_deprecated"),
        ),
    )

    class Meta:
        model = License
        fields = [
            "spdx_id",
            "name",
            "is_osi_approved",
            "is_deprecated",
            "license_groups",
        ]


class LicenseGroupFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    exclude_license_policy = NumberFilter(
        field_name="exclude_license_policy", method="get_exclude_license_policy"
    )

    def get_exclude_license_policy(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        if value is not None:
            return queryset.exclude(license_policy_items__license_policy__id=value)
        return queryset

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("is_public", "is_public"),
        ),
    )

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
            ("is_manager", "is_manager"),
        ),
    )

    class Meta:
        model = License_Group_Member
        fields = ["license_group", "user", "username", "full_name", "is_manager"]


class LicenseGroupAuthorizationGroupFilter(FilterSet):
    name = CharFilter(field_name="authorization_group__name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("authorization_group__name", "authorization_group_data.name"),
            ("license_group", "license_group"),
            ("authorization_group", "authorization_group"),
            ("is_manager", "is_manager"),
        ),
    )

    class Meta:
        model = License_Group_Authorization_Group_Member
        fields = ["license_group", "authorization_group", "name", "is_manager"]


class LicensePolicyFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("is_public", "is_public"),
        ),
    )

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
            ("is_manager", "is_manager"),
        ),
    )

    class Meta:
        model = License_Policy_Member
        fields = ["license_policy", "user", "username", "full_name", "is_manager"]


class LicensePolicyAuthorizationGroupFilter(FilterSet):
    name = CharFilter(field_name="authorization_group__name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("authorization_group__name", "authorization_group_data.name"),
            ("license_policy", "license_policy"),
            ("authorization_group", "authorization_group"),
            ("is_manager", "is_manager"),
        ),
    )

    class Meta:
        model = License_Policy_Authorization_Group_Member
        fields = ["license_policy", "authorization_group", "name", "is_manager"]
