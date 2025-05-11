import os
from celery import Celery

# celery_app = Celery(
#     "worker",
#     broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
#     backend=os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0"),
# )

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.autodiscover_tasks(["src.tasks"])
