from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.requests import Request

from api.v1.schemas.membirship_guild import GuildMembershipResponse
from api.v1.schemas.server import GuildListResponse
from api.v1.schemas.users import GuildOwnerResponse
from core.databases import DiscordDatabaseManager

router = APIRouter()


@router.get("/", response_model=List[GuildListResponse])
def get_self_guild(request: Request, session: Session = Depends(DiscordDatabaseManager.get_db_session)):
    result = session.execute(text("SELECT id, name, image FROM guild LIMIT 30"))
    guilds = result.fetchall()
    response = GuildListResponse.deserialize_from_sql_response(guilds)
    return response


@router.get("/owner/{guild_id}", response_model=GuildOwnerResponse)
def get_guild_owner(guild_id: int, session: Session = Depends(DiscordDatabaseManager.get_db_session)):
    result = session.execute(text("SELECT users.id, users.username FROM guild "
                                  "JOIN users ON users.id = guild.owner "
                                  "WHERE guild.id = :guild_id LIMIT 1"), {'guild_id': guild_id})
    users = result.fetchall()
    if len(users) == 0:
        raise HTTPException(status_code=404, detail="Guild owner not found")
    return GuildOwnerResponse.deserialize_from_sql_response(users[0])


@router.get("/membership/{guild_id}", response_model=List[GuildMembershipResponse])
def get_guild_membership(guild_id: int, session: Session = Depends(DiscordDatabaseManager.get_db_session)):
    result = session.execute(
        text("SELECT users.id, users.username, users.avatar  FROM membership_guild "
             "JOIN users ON users.id = membership_guild.user_id "
             "JOIN guild ON guild.id = membership_guild.guild_id "
             "WHERE guild.id = :guild_id LIMIT 30"), {'guild_id': guild_id})
    memberships = result.fetchall()
    print(memberships)
    if len(memberships) == 0:
        raise HTTPException(status_code=404, detail="Guild membership not found")
    response = GuildMembershipResponse.deserialize_from_sql_response(memberships)
    return response
