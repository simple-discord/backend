import datetime

from pydantic import BaseModel


class Users(BaseModel):
    __tablename__ = 'users'

    id: int
    username: str
    registration_date: datetime.datetime
    avatar: str
