"""This module is used to configure celery"""
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techprices.settings')

app = Celery('techprices')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
