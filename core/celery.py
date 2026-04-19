from celery import Celery
from dotenv import load_dotenv

from core.settings.base import local_env_file

load_dotenv(local_env_file)

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
