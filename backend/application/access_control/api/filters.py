from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter

from application.access_control.models import API_Token, Authorization_Group, User


class UserFilter(FilterSet):
    username = CharFilter(field_name="username", lookup_expr="icontains")
    full_name = CharFilter(field_name="full_name", lookup_expr="icontains")
    authorization_group = NumberFilter(field_name="authorization_groups")

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="full_name", lookup_expr="icontains")

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
            "search",
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

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"), ("oidc_group", "oidc_group")),
    )

    class Meta:
        model = Authorization_Group
        fields = ["name", "oidc_group", "search"]


class ApiTokenFilter(FilterSet):
    name = CharFilter(field_name="user__username", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("user__username", "name"),),
    )

    class Meta:
        model = API_Token
        fields = ["name"]
