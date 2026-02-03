import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from config.log import logger
from env import envSettings
from instagram_service.services.insta_message_service import InstagramMessageService

my_verify = envSettings.MY_VERIFY

@csrf_exempt
async def root():
    return JsonResponse({"message": "Hello World"}, status_code=200)


@method_decorator(csrf_exempt, name='dispatch')
class InstagramWebhookView(View):
    """Instagram webhook view"""

    VERIFY_TOKEN = envSettings.LONG_TIME_TOKEN

    async def get(self, request):
        """Webhook verification"""
        verify_token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if verify_token == self.VERIFY_TOKEN:
            return HttpResponse(
                content=challenge,
                content_type="text/plain",
                status=200
            )

        return HttpResponse(
            content="Verification failed",
            status_code=403
        )

    # instagram_service/views.py

    async def post(self, request):
        """Webhook ma'lumotlarini qabul qilish"""
        try:
            body_bytes = request.body
            body_str = body_bytes.decode('utf-8')
            data = json.loads(body_str)

            # Instagram service yaratish
            insta_service = InstagramMessageService(data)

            # Ma'lumotlarni parse qilish
            sender, message = await insta_service._parse_data()

            # Agar ignore qilinadigan event bo'lsa
            if not sender or not message:
                logger.debug("Event ignore qilindi")
                return JsonResponse({
                    'status': 'ignored',
                    'message': 'Event qayta ishlanmadi'
                }, status=200)

            # Asosiy ishlov berish
            await insta_service.manager()

            return JsonResponse({
                'status': 'success',
                'message': 'Webhook muvaffaqiyatli qayta ishlandi'
            }, status=202)

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse xatosi: {e}")
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON"
            }, status=400)

        except Exception as e:
            logger.error(f"Webhook POST error: {str(e)}", exc_info=True)
            return JsonResponse({
                "status": "error",
                "message": "Internal server error"
            }, status=500)

@csrf_exempt
async def auth_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Code not found in request"}, status=400)

    return JsonResponse({"message": "Authorization successful", "code": code}, status=200)


@csrf_exempt
async def get_access_token(request):
    import requests
    url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": envSettings.CLIENT_ID, # instagramdagi id kerak appniki emas
        "client_secret": envSettings.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": f"https://{envSettings.WEBHOOK_URL}/insta/auth/",
        "code": envSettings.SHORT_TIME_ACCESS_TOKEN,
    }

    response = requests.post(url, data=data)
    return JsonResponse({"access_token": response.json()})

@csrf_exempt
def get_long_time_token(request):
    import requests

    url = "https://graph.instagram.com/access_token"
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": envSettings.CLIENT_SECRET,
        "access_token": envSettings.SHORT_TIME_ACCESS_TOKEN,}

    response = requests.get(url, params=params)
    return JsonResponse({"data": response.json()}, status=200)