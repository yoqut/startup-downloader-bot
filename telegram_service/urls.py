from . import views
from django.urls import path

urlpatterns = [
    path('webhook/', views.telegram_webhook),
    path('set-webhook/', views.set_webhook),
]