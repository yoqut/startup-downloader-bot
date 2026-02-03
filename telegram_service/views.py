import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import telebot

from config.log import logger
from env import envSettings
from telegram_service.core import bot

from . import handlers

@csrf_exempt
@require_POST
async def telegram_webhook(request):
    try:
        body = request.body.decode('utf-8')
        json_data = json.loads(body)
        update = telebot.types.Update.de_json(json_data)
        await bot.process_new_updates([update])
        return HttpResponse('OK')

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_GET
async def set_webhook(request):
    try:
        await bot.remove_webhook()
        await bot.set_webhook(url=f"{envSettings.WEBHOOK_URL}/tele/webhook/")
        return JsonResponse({'ok': True})
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)