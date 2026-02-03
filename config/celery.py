# config/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('social_grabber')

# Redis broker uchun
app.config_from_object('django.conf:settings', namespace='CELERY')

# Redis uchun optimal sozlamalar
app.conf.broker_transport_options = {
    'visibility_timeout': 3600,  # 1 soat
    'fanout_prefix': True,
    'fanout_patterns': True,
}

app.autodiscover_tasks()