import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rrs_s.settings')

app = Celery('rrs_s')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
