import json
from json import JSONDecodeError
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text, Sequence
from sqlalchemy.orm import Session
from starlette.requests import Request
from sqlalchemy.engine import CursorResult
from starlette.responses import JSONResponse, Response

from api.v1.schemas.membirship_guild import GuildMembershipResponse
from api.v1.schemas.server import GuildListResponse, GuildPostResponse
from api.v1.schemas.users import GuildOwnerResponse
from core.databases import DiscordDatabaseManager

router = APIRouter()


@router.get("/", response_model=List[GuildListResponse], tags=["guild"])
def get_self_guild(request: Request, session: Session = Depends(DiscordDatabaseManager.get_db_session)):
    result = session.execute(text("SELECT id, name, image FROM guild LIMIT 30"))
    guilds = result.fetchall()
    response = GuildListResponse.deserialize_from_sql_response(guilds)
    return response


@router.get("/owner/{guild_id}", response_model=GuildOwnerResponse, tags=["guild"])
def get_guild_owner(guild_id: int, session: Session = Depends(DiscordDatabaseManager.get_db_session)):
    result = session.execute(text("SELECT users.id, users.username FROM guild "
                                  "JOIN users ON users.id = guild.owner "
                                  "WHERE guild.id = :guild_id LIMIT 1"), {'guild_id': guild_id})
    users = result.fetchall()
    if len(users) == 0:
        raise HTTPException(status_code=404, detail="Guild owner not found")
    return GuildOwnerResponse.deserialize_from_sql_response(users[0])


@router.get("/membership/{guild_id}", response_model=List[GuildMembershipResponse], tags=["guild"])
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


# @router.post('/', response_model=GuildPostResponse, tags=["guild"])
# def post_guild(parameters: GuildPostResponse, session: Session = Depends(DiscordDatabaseManager.get_db_session)):
#     cursor = session.execute(
#        text("INSERT INTO guild (owner, creator, creation_date, name, image) "
#         "VALUES (:owner, :creator, now(), :name, :image) RETURNING id, owner, creator, creation_date, name, image;"),
#         {'owner': parameters.owner, 'creator': parameters.creator, 'name': parameters.name, 'image': parameters.image}
#     )
#     session.commit()
#     data = cursor.fetchall()
#     # print(type(data[0]), data[0])
#     return GuildPostResponse.deserialize_from_sql(data[0])


@router.post('/', tags=["guild"], status_code=201)
async def create_guild(request: Request):
    body = await request.body()
    # TODO guild = GuildSerializer.try_serialize(body)
    print(body)
    try:
        serialized_body = json.loads(body)    # переводим в дикт (сериализатор)
        return serialized_body["name"]
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="invalid json")


@router.delete('/{id}', tags=["guild"])
def delete_guild(id: int,  session: Session = Depends(DiscordDatabaseManager.get_db_session)):
    cursor = session.execute(
        text("DELETE FROM guild "
        "WHERE id = :id"),
        {"id":id}
    )
    session.commit()
    if cursor.rowcount == 0:
        return Response(status_code=404)
    return JSONResponse(status_code=204, content={})
