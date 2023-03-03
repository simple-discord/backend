from fastapi import APIRouter

from api.v1.endpoints import (
    users, server
)

api_v1_router = APIRouter()
api_v1_router.include_router(users.router, prefix="/users")
api_v1_router.include_router(server.router, prefix="/guild")

