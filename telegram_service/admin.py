from django.contrib import admin
from .models.bot_client_model import BotClient

@admin.register(BotClient)
class BotClientAdmin(admin.ModelAdmin):
    pass
