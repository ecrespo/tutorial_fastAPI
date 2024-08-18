from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.sql.sqltypes import Integer, String

from app.conn.db import meta

users = Table(
    'users',
    meta,
    Column('_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(length=255), nullable=False),
    Column('email', String(255), nullable=False, unique=True),
    Column('password', String(255), nullable=False),
)

