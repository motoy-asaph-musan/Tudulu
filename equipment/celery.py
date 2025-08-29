# project_name/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

app = Celery('project_name')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Optional: schedule the email job daily at 9 AM
app.conf.beat_schedule = {
    'send-due-emails-every-morning': {
        'task': 'app_name.tasks.send_due_equipment_emails',
        'schedule': crontab(hour=9, minute=0),
    },
}
