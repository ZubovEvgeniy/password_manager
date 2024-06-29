from django.contrib import admin

from .models import Password


class PasswordAdmin(admin.ModelAdmin):
    list_display = ("service_name", "password")


admin.site.register(Password, PasswordAdmin)
