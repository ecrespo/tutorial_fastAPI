from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.controllers.index import user
from app.utils.WebSocket import manager
from app.utils.configs import REDIS_HOST, REDIS_PORT
import redis

#r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
r = redis.Redis(connection_pool=pool)

app = FastAPI(
title="My API with documentation",
    description="This is a very fancy FastAPI project, with auto docs for the API.",
    version="1.0.0",
    contact={
        "name": "Ernesto Crespo",
        "url": "https://medium.com/@seraph",
        "email": "ecrespo@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    doc_url_prefix="/docs",
    redoc_url="/redoc",
)


app.include_router(user)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Client {client_id}: {data}", websocket)
            await manager.broadcast(f"Client {client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected")


@app.get("/chat")
async def get():
    with open("app/index.html") as f:
        return HTMLResponse(f.read())

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Docker and Redis"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    # Example of storing data in Redis
    r.set(f"item_{item_id}", q or "No Query")
    cached_value = r.get(f"item_{item_id}")
    return {"item_id": item_id, "q": cached_value}



@app.get("/health")
async def health_check():
    return {"status": "healthy"}
