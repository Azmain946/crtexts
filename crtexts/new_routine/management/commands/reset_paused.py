from django.core.management.base import BaseCommand
from new_routine.models import Classes

class Command(BaseCommand):
    help = 'Reset paused field to False every 5 minutes'

    def handle(self, *args, **kwargs):
        Classes.objects.update(paused=False)
        self.stdout.write(self.style.SUCCESS("Succesfully reset paused field to False"))
    