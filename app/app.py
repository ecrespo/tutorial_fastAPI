from fastapi import FastAPI


app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/hello/{name}/{age}")
def hello_name_age(name: str, age: int):
    return {"message": f"Hello, {name}! You are {age} years old."}
