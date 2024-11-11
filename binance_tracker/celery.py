# binance_app/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binance_app.settings')
app = Celery('binance_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
