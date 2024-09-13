from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.app import route as route_live_scores


templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title="Live Scores",
    description="A real-time scoring application",
    version="0.1.0",
    docs_url="/api/docs",
)
# Adding CORS middleware

@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(route_live_scores)

# https://rajansahu713.medium.com/server-sent-event-sse-in-fastapi-applications-387dcd395d8d
