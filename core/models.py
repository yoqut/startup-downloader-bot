# core/models/main_client_model.py

from django.db import models

from instagram_service.models.insta_client_model import InstaClient
from telegram_service.models.bot_client_model import BotClient


class MainClient(models.Model):
    bot_client = models.ManyToManyField(BotClient)
    insta_client = models.ForeignKey(
        InstaClient,
        on_delete=models.CASCADE,
        related_name='main_clients',
        unique=True  # Bitta InstaClient uchun faqat bitta MainClient
    )

    def __str__(self):
        return str(self.insta_client)

    class Meta:
        verbose_name = "Bog'langan Foydalanuvchi"
        verbose_name_plural = "Bog'langan Foydalanuvchilar"

    async def aget_telegram_ids(self) -> list[int]:
        return [item async for item in self.bot_client.values_list('telegram_id', flat=True)]

    @classmethod
    async def aget_telegram_ids_by_insta_client_id(cls, client_id: int) -> list[int]:
        try:
            insta_client = await InstaClient.objects.aget(client_id=client_id)
            main_client = await cls.objects.aget(insta_client=insta_client)
            return await main_client.aget_telegram_ids()
        except (InstaClient.DoesNotExist, cls.DoesNotExist):
            return []