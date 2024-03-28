from django_filters import CharFilter, FilterSet, OrderingFilter

from application.access_control.models import Authorization_Group, User


class UserFilter(FilterSet):
    full_name = CharFilter(field_name="full_name", lookup_expr="icontains")

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="full_name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("full_name", "full_name"),),
    )

    class Meta:
        model = User
        fields = ["full_name", "search"]


class AuthorizationGroupFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    # search is needed for the ReferenceArrayInput field of react-admin
    search = CharFilter(field_name="name", lookup_expr="icontains")

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(("name", "name"),),
    )

    class Meta:
        model = Authorization_Group
        fields = ["name", "search"]
