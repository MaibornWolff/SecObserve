from django.db.models import BigIntegerField, CharField, DateTimeField, Index, Model

from application.background_tasks.types import Status


class Periodic_Task(Model):
    task = CharField(max_length=255)
    start_time = DateTimeField()
    duration = BigIntegerField(null=True, help_text="Duration in milliseconds")
    status = CharField(max_length=10, choices=Status.STATUS_CHOICES)
    message = CharField(max_length=255, blank=True)

    class Meta:
        indexes = [
            Index(fields=["task", "-start_time"]),
            Index(fields=["-start_time"]),
            Index(fields=["status"]),
            Index(fields=["duration"]),
        ]
