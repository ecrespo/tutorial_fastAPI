from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    celery_broker_url: str
    redis_url: str
    notification_service_url: str

    class Config:
        env_file = ".env"

settings = Settings()