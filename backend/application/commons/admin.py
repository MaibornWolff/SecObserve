from django.contrib import admin

from application.commons.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = [
        "name",
        "created",
        "user",
        "type",
        "function",
        "product",
        "observation",
    ]
