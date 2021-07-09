from celery import Celery
from celery.schedules import crontab
import os

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moth_api.settings')
app = Celery('moth_api')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'create_training_dataset': {
        'task': 'create_training_dataset',
        'schedule': crontab(hour=0, minute=50),  # Run every day at 8 AM UTC (3 AM EST)
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
