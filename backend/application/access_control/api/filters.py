from django_filters import CharFilter, FilterSet, OrderingFilter

from application.access_control.models import User


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
