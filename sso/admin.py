from django.contrib import admin

from sso.models import AutologinClient


@admin.register(AutologinClient)
class AutologinClientAdmin(admin.ModelAdmin):
    list_display = ["id", "oidc_client"]
