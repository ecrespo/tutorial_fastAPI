from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

from app.utils.LoggerSingleton import logger


# Define a Settings class that inherits from BaseSettings
class Settings(BaseSettings):
    # Define the attributes of the Settings class
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    REDIS_HOST: str
    REDIS_PORT: int

    # Load the settings from the .env file
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    """
        This function returns an instance of the Settings class.
        It uses the lru_cache decorator to cache the result,
        so that subsequent calls do not have to re-instantiate the Settings class.
    """
    return Settings()


# Get the settings
settings = get_settings()

# Assign the settings to variables
MYSQL_ROOT_PASSWORD = settings.MYSQL_ROOT_PASSWORD
MYSQL_DATABASE = settings.MYSQL_DATABASE
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

# Log that the settings have been loaded
logger.info("Settings loaded")