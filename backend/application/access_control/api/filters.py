from django.db.models import Exists
from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter

from application.access_control.models import (
    API_Token,
    Authorization_Group,
    Authorization_Group_Member,
    User,
)


class UserFilter(FilterSet):
    username = CharFilter(field_name="username", lookup_expr="icontains")
    full_name = CharFilter(field_name="full_name", lookup_expr="icontains")
    authorization_group = NumberFilter(field_name="authorization_groups")
    exclude_authorization_group = NumberFilter(
        field_name="exclude_authorization_group",
        method="get_exclude_authorization_group",
    )
    exclude_license_group = NumberFilter(
        field_name="exclude_license_group", method="get_exclude_license_group"
    )
    exclude_license_policy = NumberFilter(
        field_name="exclude_license_policy", method="get_exclude_license_policy"
    )
    exclude_product = NumberFilter(
        field_name="exclude_product", method="get_exclude_product"
    )

    def get_exclude_authorization_group(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        if value is not None:
            return queryset.exclude(authorization_groups__id=value)
        return queryset

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
            return queryset.exclude(license_policies__id=value)
        return queryset

    def get_exclude_product(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        if value is not None:
            return queryset.exclude(product_members__id=value)
        return queryset

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("username", "username"),
            ("full_name", "full_name"),
            ("is_oidc_user", "is_oidc_user"),
            ("is_active", "is_active"),
            ("is_superuser", "is_superuser"),
            ("is_external", "is_external"),
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "full_name",
            "is_oidc_user",
            "is_active",
            "is_superuser",
            "is_external",
        ]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        if not request.user.is_superuser:
            self.filters.pop("is_oidc_user")
            self.filters.pop("is_active")
            self.filters.pop("is_superuser")
            self.filters.pop("is_external")
            self.filters["ordering"] = OrderingFilter(
                fields=(
                    ("username", "username"),
                    ("full_name", "full_name"),
                ),
            )


class AuthorizationGroupFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    oidc_group = CharFilter(field_name="oidc_group", lookup_expr="icontains")
    user = NumberFilter(field_name="users")
    exclude_license_group = NumberFilter(
        field_name="exclude_license_group", method="get_exclude_license_group"
    )
    exclude_license_policy = NumberFilter(
        field_name="exclude_license_policy", method="get_exclude_license_policy"
    )
    exclude_product = NumberFilter(
        field_name="exclude_product", method="get_exclude_product"
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
            return queryset.exclude(license_policies__id=value)
        return queryset

    def get_exclude_product(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        if value is not None:
            return queryset.exclude(authorization_groups__id=value)
        return queryset

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"), ("oidc_group", "oidc_group")),
    )

    class Meta:
        model = Authorization_Group
        fields = ["name", "oidc_group"]

    def get_user(self, queryset, name, value):  # pylint: disable=unused-argument
        # field_name is used as a positional argument

        authorization_group_members = Authorization_Group_Member.objects.filter(
            user__id=value
        )
        queryset = queryset.annotate(
            member=Exists(authorization_group_members),
        )
        return queryset.filter(member=True)


class AuthorizationGroupMemberFilter(FilterSet):
    username = CharFilter(field_name="user__username", lookup_expr="icontains")
    full_name = CharFilter(field_name="user__full_name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("user__full_name", "user_data.full_name"),
            ("authorization_group", "authorization_group"),
            ("user", "user"),
            ("is_manager", "is_manager"),
        ),
    )

    class Meta:
        model = Authorization_Group_Member
        fields = ["authorization_group", "user", "is_manager", "username", "full_name"]


class ApiTokenFilter(FilterSet):
    name = CharFilter(field_name="user__username", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("user__username", "name"),),
    )

    class Meta:
        model = API_Token
        fields = ["name"]
