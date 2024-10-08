from celery import Celery
from app.configs import settings

celery = Celery(__name__, broker=settings.celery_broker_url, backend=settings.redis_url)