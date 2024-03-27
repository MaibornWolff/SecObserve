from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as Django_Group
from django.utils.translation import gettext_lazy as _

from application.access_control.forms import UserAdminChangeForm, UserAdminCreationForm
from application.access_control.models import API_Token, Authorization_Group, JWT_Secret

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_external",
                ),
            },
        ),
        (
            _("Settings"),
            {
                "fields": (
                    "setting_theme",
                    "setting_list_size",
                    "setting_list_properties",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "username",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
        "is_external",
    ]
    search_fields = ["username", "first_name", "last_name"]


@admin.register(Authorization_Group)
class AuthorizationGroupAdmin(admin.ModelAdmin):
    search_fields = ["name", "oidc_group"]
    list_display = ["name", "oidc_group"]
    ordering = ["name", "oidc_group"]
    filter_horizontal = [
        "users",
    ]


@admin.register(JWT_Secret)
class JWTSecretAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


@admin.register(API_Token)
class API_TokenAdmin(admin.ModelAdmin):
    list_display = ["user"]
    ordering = ["user"]

    def has_add_permission(self, request):
        return False


admin.site.unregister(Django_Group)
