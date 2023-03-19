import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_todo.settings')

app = Celery('django_todo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
