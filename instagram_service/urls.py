from django.urls import path

from . import views

urlpatterns = [
    path("faq/", views.root),
    path("webhook/", views.InstagramWebhookView.as_view()),
    path("auth/", views.auth_callback),
    path("get-access/", views.get_access_token),
    path("get-long-time/", views.get_long_time_token),
]