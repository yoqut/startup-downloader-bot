# instagram_service/services/insta_message_service.py

import asyncio
import logging

import aiohttp
from core.models import MainClient
from env import envSettings
from instagram_service.models.insta_client_model import InstaClient
from telegram_service.models.bot_client_model import BotClient
from telegram_service.service.telegram_message_service import TelegramMessageService

logger = logging.getLogger(__name__)


class InstagramMessageService:
    _BOT_CLIENT_NOT_FOUND = """Foydalanuvchi topilmadi !\nUshbu bot bergan koddan foydalaning\n\nt.me/YoqutMediaBot"""
    _ADD_NEW_BOT_CLIENT = """Yangi foydalanuvchi qo'shildi: {user}"""
    _ALREADY_EXISTS = """{user} allaqachon ro'yxatda!"""

    def __init__(self, data: dict):
        self.data = data
        self.access_token = envSettings.LONG_TIME_TOKEN

    async def manager(self):
        try:
            sender_id, message = await self._parse_data()
            logger.warning(await self.create_user_info(sender_id))
            # Agar parse qilinmagan bo'lsa - ignore
            if not sender_id or not message:
                logger.info("Ma'lumot ignore qilindi (sender yoki message yo'q)")
                return

            # Text xabar tekshirish
            text = message.get('text')
            if text and text.startswith('2602A'):
                await self._add_telegram_client(text, sender_id)
                return

            # Attachments tekshirish
            attachments = message.get('attachments', [])

            if not attachments:
                logger.info("Attachments yo'q - ignore qilindi")
                return

            attachment = attachments[0]
            payload = attachment.get('payload')

            await TelegramMessageService().manager(sender_id, payload)

        except Exception as e:
            logger.error(f"Manager xatosi: {e}", exc_info=True)

    async def send_instagram_reply(self, sender_id: str, message_text: str):
        url = f"https://graph.instagram.com/v22.0/17841480062253987/messages?access_token={self.access_token}"

        payload = {
            "recipient": {"id": sender_id},
            "message": {"text": message_text}
        }
        headers = {"Content-Type": "application/json"}

        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    response_data = await response.json()

                    if response.status == 200:
                        logger.info(f"✅ Instagram javobi yuborildi: {response_data}")
                    else:
                        logger.error(f"❌ Instagram xatosi ({response.status}): {response_data}")

                    return response_data
        except Exception as e:
            logger.error(f"Instagram xabar yuborishda xatolik: {e}")
            return None

    async def _add_telegram_client(self, text, sender_id):
        logger.info(f"Kod topildi: {text}")

        try:
            _, telegram_id = text.split('A')
        except ValueError:
            logger.error(f"Noto'g'ri kod formati: {text}")
            await self.send_instagram_reply(sender_id, "Noto'g'ri kod formati!")
            return

        insta_client, _ = await InstaClient.objects.aget_or_create(client_id=sender_id)

        try:
            bot_client = await BotClient.objects.aget(telegram_id=telegram_id)
        except BotClient.DoesNotExist:
            logger.info(f"BotClient topilmadi: {telegram_id}")
            await self.send_instagram_reply(sender_id, self._BOT_CLIENT_NOT_FOUND)
            return

        main_client, created = await MainClient.objects.aget_or_create(insta_client=insta_client)

        # Foydalanuvchi allaqachon qo'shilganmi tekshirish
        is_exists = await main_client.bot_client.filter(id=bot_client.id).aexists()

        if is_exists:
            logger.info(f"Foydalanuvchi allaqachon mavjud: {bot_client.full_name}")
            await self.send_instagram_reply(
                sender_id,
                self._ALREADY_EXISTS.format(user=bot_client.full_name)
            )
            return

        # Yangi foydalanuvchi qo'shish
        await main_client.bot_client.aadd(bot_client)
        logger.info(f"Yangi foydalanuvchi qo'shildi: {bot_client.full_name}")

        await self.send_instagram_reply(
            sender_id,
            self._ADD_NEW_BOT_CLIENT.format(user=bot_client.full_name)
        )

    async def _parse_data(self):
        """
        Instagram webhook datani parse qilish
        Returns: (sender_id, message) yoki (None, None) agar parse qilishda muammo bo'lsa
        """
        try:
            entry = self.data.get('entry', [])

            if not entry:
                logger.debug("Entry bo'sh - ignore")
                return None, None

            messaging = entry[0].get('messaging', [])

            if not messaging:
                logger.debug("Messaging bo'sh - ignore")
                return None, None

            messaging_event = messaging[0]

            # Sender ID ni olish
            sender_id = messaging_event.get('sender', {}).get('id')

            # Message borligini tekshirish
            message = messaging_event.get('message')

            # Agar message yo'q bo'lsa, boshqa eventlar (delivery, read, reaction)
            if not message:
                event_type = self._detect_event_type(messaging_event)
                logger.debug(f"Message yo'q. Event turi: {event_type} - ignore qilindi")
                return None, None

            logger.info(f"📨 Yangi xabar: Sender={sender_id}")
            return sender_id, message

        except (IndexError, KeyError) as e:
            logger.warning(f"Parse qilishda xatolik: {e}")
            return None, None

    def _detect_event_type(self, event: dict) -> str:
        """Event turini aniqlash"""
        if 'delivery' in event:
            return 'delivery'
        elif 'read' in event:
            return 'read'
        elif 'reaction' in event:
            return 'reaction'
        elif 'echo' in event:
            return 'echo'
        else:
            return 'unknown'

    # instagram_service/services/insta_message_service.py

    async def create_user_info(self, user_id: str) -> dict:

        url = f"https://graph.instagram.com/v24.0/{user_id}"

        params = {
            'fields': 'id,username,name,profile_pic,follower_count,is_verified_user',
            'access_token': self.access_token
        }

        if await InstaClient.user_exists(user_id):
            return f"User {user_id} already exists"

        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        logger.info(f"✅ User ma'lumotlari olindi: {user_data}")
                        await InstaClient().create_from_webhook(user_data)
                        return user_data
                    else:
                        error_data = await response.json()
                        logger.error(f"❌ User ma'lumotlarini olishda xatolik ({response.status}): {error_data}")
                        return None
        except Exception as e:
            logger.error(f"User info olishda xatolik: {e}")
            return None