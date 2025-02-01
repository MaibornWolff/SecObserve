from django.db.models import Subquery
from django_filters import BooleanFilter, CharFilter, FilterSet, OrderingFilter

from application.commons.models import Notification, Notification_Read
from application.commons.services.global_request import get_current_user


class NotificationFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    message = CharFilter(field_name="message", lookup_expr="icontains")
    function = CharFilter(field_name="function", lookup_expr="icontains")
    exclude_already_read = BooleanFilter(
        field_name="exclude_already_read", method="get_exclude_already_read"
    )

    def get_exclude_already_read(
        self, queryset, field_name, value
    ):  # pylint: disable=unused-argument
        # field_name is used as a positional argument
        user = get_current_user()
        if not user:
            return queryset

        if value:
            return queryset.exclude(
                id__in=Subquery(
                    Notification_Read.objects.filter(user=user).values_list(
                        "notification_id", flat=True
                    )
                )
            )

        return queryset

    ordering = OrderingFilter(
        fields=(
            ("name", "name"),
            ("created", "created"),
            ("message", "message"),
            ("type", "type"),
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
            "type",
            "function",
            "product",
            "observation",
            "user",
        ]
