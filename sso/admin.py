from django.contrib import admin

from sso.models import AutologinClient, User


@admin.register(AutologinClient)
class AutologinClientAdmin(admin.ModelAdmin):
    list_display = ["id", "oidc_client"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
