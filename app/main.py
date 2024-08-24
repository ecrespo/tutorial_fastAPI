import time
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.conn.database import init_db, close_db
from app.controllers.Tasks import task_router
from app.middlewares.log_requests import log_requests
from app.utils.LoggerSingleton import logger




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Acción al iniciar
    logger.info("Connecting to MongoDB...")
    await init_db()
    yield
    # Acción al cerrar
    logger.info("Disconnecting from MongoDB...")
    await close_db()

# @app.on_event("startup")
# async def connect():
#     logger.info("Connecting to MongoDB...")
#     await init_db()
#
#
# @app.on_event("shutdown")
# async def disconnect():
#     logger.info("Disconnecting from MongoDB...")
#     await close_db()

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
    lifespan=lifespan,
)

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    return await log_requests(request, call_next)


@app.get("/")
def read_root():
    logger.info("Read root request...")
    return {"message": "Welcome to FastAPI with Docker and Redis"}



@app.get("/health")
async def health_check():
    logger.info("Health check request...")
    return {"status": "healthy"}


app.include_router(task_router, prefix="/tasks")