from django.contrib import admin

from application.rules.models import Rule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
