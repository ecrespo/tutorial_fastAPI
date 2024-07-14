from enum import Enum
from fastapi import FastAPI, Path


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


@app.get("/users/{_id}")
async def get_user(_id: int = Path(..., ge=1, lt=100)):
    return {"_id": _id}


@app.get("/license-plates/{license}")
async def get_license_plate(license: str = Path(..., min_length=9, max_length=9)):
    return {"license": license}


@app.get("/license-plates/{license}")
async def get_license_plate(license: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}$")):
    return {"license": license}