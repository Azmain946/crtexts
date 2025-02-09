from celery import shared_task
from django.utils import timezone
from .models import Classes
from celery.schedules import crontab
from celery import Celery


@shared_task
def reset_classes():
    Classes.objects.all().update(paused=False)


