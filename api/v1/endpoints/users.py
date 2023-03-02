from typing import List

from fastapi import FastAPI, APIRouter

from api.v1.schemas.users import Users

router = APIRouter()


@router.get("/", response_model=List[Users])
async def get_users():
    return {"message": "Hello World"}

@router.get("/{id}", response_model=Users)
async def get_users_id(id: int):
    return {"message": "Hello World"}
