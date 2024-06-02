import os

from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jaggery.settings")

app = Celery("jaggery")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Every minute
    "Fetch Expired Catalog Contents": {
        "task": "sachet.tasks.fetch_expired_catalogs_content",
        "schedule": timedelta(seconds=60),
    },
    "Celery Result Cleanup": {
        "task": "celery.backend_cleanup",
        "schedule": crontab(hour=12, minute=0),
    },
}
