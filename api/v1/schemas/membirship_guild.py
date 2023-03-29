from collections import defaultdict
from typing import List, Tuple, Iterable

from pydantic import BaseModel
from sqlalchemy import Row


class GuildMembershipResponse(BaseModel):
    user_id: int
    username: str
    avatar: str

    @staticmethod
    def deserialize_from_sql_response(sql_response: Iterable):
        membership = defaultdict(list)
        result = []
        duplicates = set()
        for row in sql_response:
            if row[0] in membership:
                duplicates.add(row)
            membership[row[0]].append({"user_id": row[0], "avatar": row[2]})
        for row in sql_response:
            if row in duplicates:
                continue
            result.append({
                "user_id": row[0],
                "username": row[1],
                "avatar": row[2],
            })
        return result
