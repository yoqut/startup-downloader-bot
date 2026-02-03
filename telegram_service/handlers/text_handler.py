import telebot

from telegram_service.core import bot


@bot.message_handler(content_types=['text', 'photo', 'video'])
async def text_handler(message: telebot.types.Message):
    await bot.send_message(
        message.chat.id,
        message.forward_from_chat)