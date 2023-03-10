import datetime
from collections import defaultdict
from typing import List, Tuple

from pydantic import BaseModel
from sqlalchemy import Row


class Users(BaseModel):
    id: int
    username: str
    registration_date: datetime.datetime
    avatar: str


class GuildOwnerResponse(BaseModel):
    id: int
    username: str

    @staticmethod
    def deserialize_from_sql_response(row: Row) -> dict:
        return {
            "id": row.id,
            "username": row.username,
        }


class UserGuildListResponse(BaseModel):
    guild_id: int
    name: str
    image: str

    @staticmethod
    def deserialize_from_sql_response(sql_response: List[Tuple]):
        membership = defaultdict(list)
        result = []
        duplicates = set()
        for row in sql_response:
            if row[0] in membership:
                duplicates.add(row)
            membership[row[0]].append({"guild_id": row[0], "image": row[2]})
        for row in sql_response:
            if row in duplicates:
                continue
            result.append({
                "guild_id": row[0],
                "name": row[1],
                "image": row[2],
            })
        return result
