import beanie
import motor.motor_asyncio

from app.utils.LoggerSingleton import logger
from app.utils.configs import MONGO_URI
from app.models.Tasks import Task


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            logger.info("Database instance created")
            cls._instance.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        return cls._instance


async def init_db():
    db_instance = Database()
    await beanie.init_beanie(database=db_instance.client.db_name, document_models=[Task])


async def close_db():
    db_instance = Database()
    db_instance.client.close()
    logger.info("Database connection closed")