from app.conn.db import engine, meta

meta.create_all(engine)