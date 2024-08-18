from fastapi import APIRouter
import strawberry
from strawberry.asgi import GraphQL

from app.type.users import Query, Mutation


user = APIRouter()

schema = strawberry.Schema(Query, Mutation)

graphql_app = GraphQL(schema)

user.add_route("/graphql", graphql_app)
