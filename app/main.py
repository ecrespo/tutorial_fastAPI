from fastapi import FastAPI
from app.controllers.index import user

app = FastAPI()


app.include_router(user)
