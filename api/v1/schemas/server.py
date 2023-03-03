from collections import defaultdict
from typing import List, Tuple

from pydantic import BaseModel
from sqlalchemy import Row


class GuildListResponse(BaseModel):

    id: int
    name: str
    image: str

    @staticmethod
    def deserialize_from_sql_response(sql_response: List[Tuple]):
        guild = defaultdict(list)
        result = []
        duplicates = set()
        for row in sql_response:
            if row[0] in guild:
                duplicates.add(row)
            guild[row[0]].append({"id": row[0], "image": row[2]})
        for row in sql_response:
            if row in duplicates:
                continue
            result.append({
                "id": row[0],
                "name": row[1],
                "image": row[2],
            })
        return result
