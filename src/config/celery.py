import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='config.settings')

app = Celery('config')

# Using a string here means that the worker does not need to serialize
# the configuration object to child processes.
# - namespace='CELERY' means that all Celery-related configuration keys
# must be prefixed with `CELERY_`.
app.config_from_object(obj='django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()