import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
app = Celery("main")


app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'every': {
        'task': 'telegram_bot.tasks.repeat_order_make',
        'schedule': crontab(minute='0', hour='2,4,6,8,10,12,14,16,18,20,22')
    },
}