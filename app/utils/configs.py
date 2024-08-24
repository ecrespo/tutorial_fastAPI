from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from functools import lru_cache

from app.utils.LoggerSingleton import logger


# Define a Settings class that inherits from BaseSettings
class Settings(BaseSettings):
    # Define the attributes of the Settings class
    MONGO_URI: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    API_KEY: str
    URL_DB_API: AnyHttpUrl
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
MONGO_URI = settings.MONGO_URI
MONGO_INITDB_ROOT_USERNAME = settings.MONGO_INITDB_ROOT_USERNAME
MONGO_INITDB_ROOT_PASSWORD = settings.MONGO_INITDB_ROOT_PASSWORD
API_KEY = settings.API_KEY
URL_DB_API = settings.URL_DB_API
# Log that the settings have been loaded
logger.info("Settings loaded")