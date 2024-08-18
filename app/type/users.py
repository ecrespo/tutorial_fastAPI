import strawberry
import typing

from app.conn.db import conn
from app.models.index import users
#from app.models.users import users


@strawberry.type
class User:
    _id: int
    name: str
    email: str
    password: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self, info, _id:int) -> User:
        return conn.execute(users.select().where(users.c._id == _id)).fetchone()

    @strawberry.field
    def users(self, info) -> typing.List[User]:
        return conn.execute(users.select()).fetchall()



@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, info, name:str, email:str, password:str) -> int:
        user = {
            'name': name,
            'email': email,
            'password': password
        }

        result = conn.execute(users.insert().values(user))
        user['_id'] = result.lastrowid

        return int(user['_id'])

    @strawberry.mutation
    def update_user(self, info, _id:int, name:str = None, email:str = None, password:str = None) -> str:
        user = {
            'name': name,
            'email': email,
            'password': password
        }

        result = conn.execute(users.update().where(users.c._id == _id).values(user))

        return str(result.rowcount) + " rows updated"

    @strawberry.mutation
    def delete_user(self, info, _id:int) -> bool:
        result = conn.execute(users.delete().where(users.c._id == _id))

        return result.rowcount > 0
