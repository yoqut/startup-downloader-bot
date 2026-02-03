from telebot.async_telebot import AsyncTeleBot
from env import envSettings

bot = AsyncTeleBot(
    token=envSettings.TELEGRAM_BOT_TOKEN,
    parse_mode="HTML"
)

