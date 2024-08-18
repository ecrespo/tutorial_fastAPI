from sqlalchemy import create_engine, MetaData

from app.utils.LoggerSingleton import logger
from app.utils.configs import MYSQL_ROOT_PASSWORD, MYSQL_DATABASE


class DatabaseConnection:
    _instance = None
    _engine = None
    _meta = None
    _conn = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

            # Initialize the connection
            url = f'mysql+pymysql://root:{MYSQL_ROOT_PASSWORD}@db:3306/{MYSQL_DATABASE}'
            logger.info(f"Connecting to database at {url}")
            cls._engine = create_engine(url)
            cls._meta = MetaData()
            cls._conn = cls._engine.connect()

        return cls._instance

    @property
    def engine(self):
        return self._engine

    @property
    def meta(self):
        return self._meta

    @property
    def conn(self):
        return self._conn


# Usage of Singleton pattern for connection
db = DatabaseConnection()
engine = db.engine
meta = db.meta
conn = db.conn
