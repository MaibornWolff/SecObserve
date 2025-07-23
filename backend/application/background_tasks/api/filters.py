from django_filters import CharFilter, ChoiceFilter, FilterSet, OrderingFilter

from application.background_tasks.models import Periodic_Task
from application.background_tasks.types import Status


class PeriodicTaskFilter(FilterSet):
    task = CharFilter(field_name="task", lookup_expr="icontains")
    status = ChoiceFilter(field_name="status", choices=Status.STATUS_CHOICES)

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("task", "task"),
            ("start_time", "start_time"),
            ("status", "status"),
            ("duration", "duration"),
        ),
    )

    class Meta:
        model = Periodic_Task
        fields = ["task", "status", "start_time", "duration"]
        order_by = ["-start_time"]
