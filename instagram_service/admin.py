from django.contrib import admin
from .models.insta_client_model import InstaClient

@admin.register(InstaClient)
class InstaClientAdmin(admin.ModelAdmin):
    pass

