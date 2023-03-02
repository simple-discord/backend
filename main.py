from fastapi import FastAPI

from api.v1.api import api_v1_router

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/swagger")
app.include_router(api_v1_router, prefix='/api/v1')
