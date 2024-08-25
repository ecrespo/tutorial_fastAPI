import httpx
import asyncio
from datetime import timedelta

from fastapi import FastAPI, Request, Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse

from contextlib import asynccontextmanager

from app.conn.database import init_db, close_db
from app.controllers.TasksController import task_router
from app.controllers.UsersController import users_router
from app.middlewares.log_requests import log_requests
from app.utils.LoggerSingleton import logger
from app.utils.configs import API_KEY, URL_DB_API, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.AsyncHttpx import get_client
from app.middlewares.verify_api_key import APIKeyVerifier
from app.utils.auth import authenticate_user, create_access_token, get_current_active_user, fake_users_db
from app.models.UsersModel import Token, User


api_key_verifier = APIKeyVerifier([API_KEY])


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


@app.get("/bienvenida", response_class=HTMLResponse)
def welcome():
    logger.info("Read root request...")
    html_content = """
        <html>
            <head>
                <title>Welcome</title>
            </head>
            <body>
                <h1>Welcome to FastAPI with Docker</h1>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/")
def read_root():
    logger.info("Read root request...")
    return RedirectResponse(url="/redoc/")



@app.get("/health")
async def health_check():
    logger.info("Health check request...")
    return {"status": "healthy"}


@app.get("/hola")
def hola(api_key: str = Security(api_key_verifier)) -> dict:
    logger.info("Read hola request...")
    return {"message": "Hola mundo!"}




@app.get("/prueba")
async def prueba(page: int = 0,client: httpx.AsyncClient = Depends(get_client),api_key: str = Security(api_key_verifier)):
    logger.info("Read prueba request...")
    try:
        caracters_url = f"{URL_DB_API}/character/?page={page}"
        response = await client.get(caracters_url,timeout=None)
        response_json = response.json()

        if response.status_code == 200:
            return response_json["results"]
        if response.status_code == 400:
            message = response_json.get("mensajes", "Error en la solicitud")[0]["mensaje"]
            logger.error(f"Error en la solicitud: {message}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except httpx.RequestError as e:
        logger.error(f"Error en la solicitud: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    except httpx.ReadTimeout as e:
        logger.error(f"Tiempo de espera excedido: {e}")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Tiempo de espera excedido")


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



app.include_router(task_router, prefix="/tasks")
app.include_router(users_router, prefix="/users")