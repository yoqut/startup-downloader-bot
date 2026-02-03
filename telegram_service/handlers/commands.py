from telebot.types import Message

from telegram_service.core import bot
from telegram_service.models.bot_client_model import BotClient


# ====== TEXTS ======
TEXT_START = (
    "🎬 <b>Instagramdan video yuklab olish — oson va tez!</b>\n\n"
    "Quyidagi buyruqlar:\n"
    "• /help — To‘liq qo‘llanma\n"
    "• /insta — Shaxsiy kod olish"
)

TEXT_HELP = (
    "🧩 <b>Botni Instagram profil bilan bog‘lash</b>\n\n"
    "1️⃣ <b>/insta</b> buyrug‘ini yuboring\n"
    "2️⃣ Bot bergan <b>kod</b>ni nusxalang\n"
    "3️⃣ Kodni ushbu profilga yuboring:\n"
    "   🔗 <b>instagram.com/yoqutmedia</b>\n"
    "4️⃣ Endi yoqqan videoni <b>instagram.com/yoqutmedia</b> profiliga yuboring\n\n"
    "✅ Video bot orqali sizga qaytib keladi."
)

TEXT_INSTA = (
    "🔐 <b>Sizning shaxsiy kod raqamingiz:</b>\n"
    "<code>{prefix}{code}</code>\n\n"
    "📩 Ushbu kodni Instagramdagi <b>https://www.instagram.com/yoqutmedia</b> profiliga yuboring.\n"
    "So‘ng videoni ham shu profilga yuborsangiz — bot sizga qaytarib beradi."
)

CODE_PREFIX = "2602A"


# ====== HELPERS ======
async def send(chat_id: int, text: str):
    """Barcha xabarlar uchun yagona send wrapper (clean & consistent)."""
    return await bot.send_message(
        chat_id,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


# ====== HANDLERS ======
@bot.message_handler(commands=["start"])
async def start_handler(message: Message):
    await BotClient.create_user(message)  # idempotent bo'lsa ideal
    await send(message.chat.id, TEXT_START)


@bot.message_handler(commands=["help"])
async def help_handler(message: Message):
    await send(message.chat.id, TEXT_HELP)


@bot.message_handler(commands=["insta"])
async def insta_handler(message: Message):
    code = message.from_user.id
    await send(message.chat.id, TEXT_INSTA.format(prefix=CODE_PREFIX, code=code))
