from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

import uptime.models


@admin.register(uptime.models.Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ("__str__", "message")


admin.site.register(uptime.models.Domain)
admin.site.register(uptime.models.User, UserAdmin)
