from typing import List

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.v1.schemas.users import Users, UserGuildListResponse
from core.databases import DiscordDatabaseManager

router = APIRouter()


@router.get("/", response_model=List[Users])
async def get_users():
    return {"message": "Hello World"}

@router.get("/{id}", response_model=Users)
async def get_users_id(id: int):
    return {"message": "Hello World"}


@router.get("/guild_list/{user_id}", response_model=List[UserGuildListResponse])
def get_user_guild_list(user_id: int, session: Session = Depends(DiscordDatabaseManager.get_db_session)):
    result = session.execute(
        text("SELECT guild.id, guild.name, guild.image FROM membership_guild "
             "JOIN users ON users.id = membership_guild.user_id "
             "JOIN guild ON guild.id = membership_guild.guild_id "
             "WHERE users.id = :user_id LIMIT 30"), {'user_id': user_id})
    guild_lists = result.fetchall()
    print(guild_lists)
    if len(guild_lists) == 0:
        raise HTTPException(status_code=404, detail="Guild membership not found")
    response = UserGuildListResponse.deserialize_from_sql_response(guild_lists)
    return response
