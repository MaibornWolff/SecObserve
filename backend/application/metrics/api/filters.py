from datetime import timedelta

from django.utils import timezone
from django_filters import ChoiceFilter, FilterSet, OrderingFilter

from application.metrics.models import Product_Metrics
from application.metrics.services.age import AGE_CHOICES, get_days


class ProductMetricsFilter(FilterSet):
    age = ChoiceFilter(field_name="age", method="get_age", choices=AGE_CHOICES)

    ordering = OrderingFilter(
        fields=(
            ("product", "product"),
            ("date", "date"),
        ),
    )

    class Meta:
        model = Product_Metrics
        fields = [
            "product",
        ]

    def get_age(self, queryset, field_name, value):  # pylint: disable=unused-argument
        # field_name is used as a positional argument by django-filter

        days = get_days(value)

        if days is None:
            return queryset

        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_threshold = today - timedelta(days=int(days))
        return queryset.filter(date__gte=time_threshold)
