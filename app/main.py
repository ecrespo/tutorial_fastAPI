from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.controllers.index import user
from app.utils.WebSocket import manager

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
