from enum import Enum
from fastapi import FastAPI


class TipoUsuarioEnum(str, Enum):
    ESTANDARD = "estandard"
    ADMIN = "admin"

app = FastAPI()

@app.get("/hola")
def hola():
    return {"mensaje": "Hola, Mundo!"}


@app.get("/hello/{nombre}")
def hola_nombre(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}


@app.get("/hello/{name}/{age}")
def hello_name_age(name: str, age: int):
    return {"message": f"Hello, {name}! You are {age} years old."}


@app.get("/users/{tipo}/{_id}")
async def get_user(tipo: TipoUsuarioEnum, _id: int):
    return {"tipo": tipo, "_id": _id}

