from django.contrib import admin

from application.vex.models import VEX_Counter


@admin.register(VEX_Counter)
class VEXCounterAdmin(admin.ModelAdmin):
    search_fields = ["document_id_prefix", "year"]
    list_display = ["document_id_prefix", "year", "counter"]
    ordering = ["document_id_prefix", "year"]
