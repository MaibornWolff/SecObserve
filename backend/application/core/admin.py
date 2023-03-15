from django.contrib import admin
from django.contrib.auth.models import Group
from application.core.models import Product_Member, Product, Parser, Observation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(Product_Member)
class ProductMemberAdmin(admin.ModelAdmin):
    list_display = ["product", "user"]


@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["product", "title"]


admin.site.unregister(Group)
