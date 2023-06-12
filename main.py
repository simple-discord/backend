from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import api_v1_router
from core.databases import DiscordDatabaseManager

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/swagger")
app.include_router(api_v1_router, prefix='/api/v1')


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    DiscordDatabaseManager.init_pool()

@app.on_event("shutdown")
def shutdown():
    ...