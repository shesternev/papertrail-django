import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'papertrail.settings')

app = Celery('papertrail')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'mailing-to-active-users-every-week': {
        'task': 'mailing.tasks.mailing_to_active_users',
        'schedule': crontab(minute=0, hour=0, day_of_week=0),
    },
    'delete-old-carts-every-day': {
        'task': 'cart.tasks.delete_old_carts',
        'schedule': crontab(hour=0, minute=0),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
