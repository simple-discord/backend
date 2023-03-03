import sys
from typing import List

from sqlalchemy import create_engine, text, Text, TextClause

from sql_app.config import get_settings

up_migrations: List[TextClause] = [
    text("DROP TABLE friends"),
    text("DROP TABLE message_on_channel_group"),
    text("DROP TABLE membership_channel_group"),
    text("DROP TABLE channel_group"),
    text("DROP TABLE message_on_guild_channel"),
    text("DROP TABLE guild_channel"),
    text("DROP TABLE membership_guild"),
    text("DROP TABLE guild"),
    text("DROP TABLE session"),
    text("DROP TABLE users"),
    ]

s = get_settings()

connection_str = f'postgresql://{s.DB_USER}:{s.DB_PASS}@{s.DB_HOST}:5432/{s.DB_NAME}'
print(connection_str)
engine = create_engine(connection_str)
with engine.connect() as con:

    try:
        for migration in up_migrations:
            print(migration)
            con.execute(migration)
        con.commit()
    except Exception as e:
        print(e, file=sys.stderr)
        con.rollback()


