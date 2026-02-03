import asyncio
import logging
from typing import Union

from core.models import MainClient
from telegram_service.core import bot

logger = logging.getLogger(__name__)


class TelegramMessageService:
    _ADS_TEXT = """\n\n📥 Yuklab olindi: @social_video_grabberbot\n📸 Instagram: instagram.com/yoqut.service"""

    async def send_video_by_url(self,
                                sender_id: Union[str, int],
                                video_url: str,
                                video_title: str):

        telegram_id_list = await MainClient.aget_telegram_ids_by_insta_client_id(sender_id)

        try:
            if not telegram_id_list:
                logger.warning(f"Instagram user {sender_id} uchun telegram userlar topilmadi")
                return

            logger.warning(f"Reel yuborilmoqda: {len(telegram_id_list)} ta telegram userga")

            for telegram_id in telegram_id_list:
                try:
                    await asyncio.sleep(0.5)
                    # caption = video_title[:800].replace("@", "instagram.com/") + self._ADS_TEXT if video_title else self._ADS_TEXT
                    caption = self._ADS_TEXT

                    await bot.send_video(telegram_id, video_url, caption=caption)
                    logger.warning(f"✅ Reel yuborildi: {telegram_id}")

                except Exception as send_error:
                    logger.error(f"❌ Telegram {telegram_id} ga yuborishda xatolik: {send_error}")
        except Exception as error:
            logger.error(error)


