import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrexts.settings')

app = Celery('ctrexts')

# Load settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# Celery Beat Schedule for running tasks every 5 minutes
from celery.schedules import crontab

app.conf.beat_schedule = {
    'reset-classes-every-5-minutes': {
        'task': 'new_routine.tasks.reset_classes',
        'schedule': crontab(minute='*/5'),  # Runs every 5 minutes
    }
}
