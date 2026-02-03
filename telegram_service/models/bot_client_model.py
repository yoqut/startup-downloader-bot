# telegram_service/models/bot_client_model.py

from django.db import models
from telebot.types import Message
from config.log import logger


class BotClient(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    language_code = models.CharField(max_length=2, default="uz")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.language_code})"

    class Meta:
        verbose_name = "Telegram Foydalanuvchisi"
        verbose_name_plural = "Telegram Foydalanuvchilari"

    @classmethod
    async def create_user(cls, data: Message) -> "BotClient":
        """
        Create or update a BotClient from a Telegram Message.
        telegram_id is the only lookup key — name/username go in defaults
        so updates work correctly if the user changes their profile.
        """
        try:
            client, _ = await cls.objects.aupdate_or_create(
                telegram_id=data.from_user.id,  # ← lookup
                defaults={                       # ← everything else updates
                    "full_name": data.from_user.full_name,
                    "username": data.from_user.username or None,
                },
            )
            return client
        except Exception as exc:
            logger.error("BotClient create error: %s", exc, exc_info=True)
            raise