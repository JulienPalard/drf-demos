from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
import uptime.models

admin.site.register(uptime.models.Check)
admin.site.register(uptime.models.Domain)
admin.site.register(uptime.models.User, UserAdmin)
