import os
from celery import Celery
from celery.schedules import crontab

"""Этот файл будет чисто под celery здесь ну будет тасок а в основном какие-то настройки или таймеры для тасок"""
"""redis: redis-server
    celery worker: celery --app <name app[rrs_s]> worker -l info
    celery timer: celery --app <name app[rrs_s]> beat -l info
    
                                                                ВАЖНО!!! Чтобы работал таймер нужно, чтобы был запущен воркер вместе!!!"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rrs_s.settings')

app = Celery('rrs_s')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Важно!!! Чтобы работал "таймер" должен быть запущен воркер
app.conf.beat_schedule = {  # Это для того чтобы наши некоторые таски работали по таймеру
    'check_new_video_every_30_minute': {  # Как будет называться наш "таймер"
        'task': 'main.tasks.check_videos_and_create',  # какую таску он будет вызывать
        'schedule': crontab(minute='*/30'),  # и с какой переодичностью
    }
}
