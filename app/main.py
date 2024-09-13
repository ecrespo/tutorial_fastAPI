from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer


from app.api.app import route as route_live_scores


templates = Jinja2Templates(directory="app/templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI(
    title="Live Scores",
    description="A real-time scoring application",
    version="0.1.0",
    docs_url="/custom-docs",
    redoc_url="/custom-redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide models section by default
        "docExpansion": "none",  # Collapse all sections by default
    },
    # swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    # swagger_ui_init_oauth={
    #     "clientId": "your-client-id",
    #     "appName": "Custom Swagger UI",
    # },
    # redoc_options={
    #     "hide-hostname": True,  # Hide the hostname
    #     "expand-responses": "200,201",  # Automatically expand responses with status codes 200 and 201
    #     "theme": {
    #         "colors": {
    #             "primary": {
    #                 "main": "#00bcd4"
    #             }
    #         }
    #     }
    # }
)
# Adding CORS middleware

@app.get("/", tags=["homepage"],response_class=HTMLResponse, summary="Welcome to the Live Scores application", description="Welcome to the Live Scores application"  )
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
