from app.models.users import users
from app.conn.db import engine, meta

meta.create_all(engine)