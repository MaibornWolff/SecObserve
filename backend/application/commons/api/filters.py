from django_filters import CharFilter, FilterSet, OrderingFilter

from application.commons.models import Notification


class NotificationFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    message = CharFilter(field_name="message", lookup_expr="icontains")
    function = CharFilter(field_name="function", lookup_expr="icontains")

    ordering = OrderingFilter(
        fields=(
            ("name", "name"),
            ("created", "created"),
            ("message", "message"),
            ("function", "function"),
            ("product__name", "product_name"),
            ("observation__title", "observation_title"),
            ("user__full_name", "user_full_name"),
        ),
    )

    class Meta:
        model = Notification
        fields = [
            "name",
            "created",
            "message",
            "function",
            "product",
            "observation",
            "user",
        ]
