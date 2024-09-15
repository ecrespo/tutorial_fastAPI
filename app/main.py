from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse, HTMLResponse,JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette_csrf import CSRFMiddleware
from starlette_context.middleware import ContextMiddleware
from starlette_context import context
from fastapi_g_context import GlobalsMiddleware, g

import time
import logging
import asyncio


# Extract constants for better readability and configuration management
TEMPLATES_DIR = "app/templates"
TOKEN_URL = "token"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

# Define application metadata
APP_METADATA = {
    "title": "Live Scores",
    "description": "A real-time scoring application",
    "version": "0.1.0",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "swagger_ui_parameters": {
        "defaultModelsExpandDepth": -1,  # Hide models section by default
        "docExpansion": "none",  # Collapse all sections by default
    },
}

# Initialize FastAPI app
app = FastAPI(**APP_METADATA)

# Define CORS configuration
CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            response = JSONResponse({"error": str(e)}, status_code=500)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if timestamp > current_time - self.window]

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(status_code=429, content={"error": "Too many requests"})

        self.requests[client_ip].append(current_time)
        return await call_next(request)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if not token or token != "Bearer valid-token":
            return PlainTextResponse(status_code=401, content="Unauthorized")
        return await call_next(request)


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


logger = logging.getLogger("my_logger")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return PlainTextResponse(status_code=504, content="Request timed out")


class TrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.endswith("/"):
            return RedirectResponse(url=f"{request.url.path}/")
        return await call_next(request)


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, whitelist):
        super().__init__(app)
        self.whitelist = whitelist

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        if client_ip not in self.whitelist:
            return PlainTextResponse(status_code=403, content="IP not allowed")
        return await call_next(request)


def configure_middleware(app):
    """Configure middleware for the FastAPI app."""
    app.add_middleware(CORSMiddleware, **CORS_CONFIG)
    app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses larger than 1000 bytes
    # app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "*.example.com"])
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RateLimitMiddleware, max_requests=5, window=60)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(CustomHeaderMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(TimeoutMiddleware, timeout=5)
    app.add_middleware(TrailingSlashMiddleware)
    app.add_middleware(IPWhitelistMiddleware, whitelist=["127.0.0.1", "192.168.1.1"])
    app.add_middleware(ProxyHeadersMiddleware)
    app.add_middleware(CSRFMiddleware, secret="__CHANGE_ME__")
    app.add_middleware(ContextMiddleware)
    app.add_middleware(GlobalsMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/set/")
async def set_session_data(request: Request):
    request.session['user'] = 'john_doe'
    return {"message": "Session data set"}

@app.get("/get/")
async def get_session_data(request: Request):
    user = request.session.get('user', 'guest')
    return {"user": user}


@app.get("/error")
async def root():
    raise ValueError("This is an error!")


@app.get("/root")
async def root():
    await asyncio.sleep(10)  # Simulates a long-running process
    return {"message": "This won't be reached if the timeout is less than 10 seconds."}


@app.get("/hello/")
async def hello():
    return {"message": "Hello with trailing slash!"}


@app.get("/proxy")
async def root(request: Request):
    return {"client_ip": request.client.host}

@app.get("/cookie")
async def root(request: Request):
    return {"message": request.cookies.get('csrftoken')}


async def set_globals() -> None:
    context["username"] = "chris"


@app.get("/context", dependencies=[Depends(set_globals)])
async def info():
    return JSONResponse(context.data)


async def set_globals() -> None:
    g.username = "JohnDoe"
    g.request_id = "123456"
    g.is_admin = True

@app.get("/globals", dependencies=[Depends(set_globals)])
async def info():
    return {"username": g.username, "request_id": g.request_id, "is_admin": g.is_admin}

# Apply configurations
configure_middleware(app)