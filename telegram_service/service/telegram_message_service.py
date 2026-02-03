import asyncio
import logging

from core.models import MainClient
from telegram_service.core import bot

logger = logging.getLogger(__name__)


class TelegramMessageService:
    _ADS_TEXT = """\n\n📥 Yuklab olindi: @YoqutMediaBot\n📸 Instagram: instagram.com/YoqutMedia"""

    async def manager(self, sender_id: int, payload: dict) -> None:
        video_url = payload.get("url", "")
        return await self._send_share(sender_id, video_url)

    async def _send_share(self, sender_id: int, video_url: str) -> None:
        telegram_id_list = await MainClient.aget_telegram_ids_by_insta_client_id(sender_id)
        if not telegram_id_list:
            return "Telegram ID topilmadi avval telegramni ulang. \n\nt.me/YoqutMediaBot"

        for telegram_id in telegram_id_list:
            await asyncio.sleep(0.5)
            caption = self._ADS_TEXT
            try:
                return await bot.send_video(telegram_id, video=video_url, caption=caption)
            except Exception as e:
                logger.error(e)
                try:
                    return await bot.send_photo(sender_id, photo=video_url, caption=caption)
                except Exception as e:
                    logger.error(e)
                    return





