from django.contrib import admin

from core.models import MainClient


@admin.register(MainClient)
class MainClientAdmin(admin.ModelAdmin):
    pass
