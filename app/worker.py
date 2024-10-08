from app.celery_app import celery
from app.configs import settings
from app.main import send_notification

celery.conf.update(
    broker_url=settings.celery_broker_url,
    result_backend=settings.redis_url,
)

if __name__ == "__main__":
    celery.worker_main()