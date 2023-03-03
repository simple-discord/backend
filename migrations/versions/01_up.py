import sys
from typing import List

from sqlalchemy import create_engine, text, Text, TextClause

from sql_app.config import get_settings

up_migrations: List[TextClause] = [
    text("CREATE TABLE users ("
         "id bigint generated always as identity primary key,"
         "username varchar(50) NOT NULL UNIQUE,"
         "registration_date timestamp NOT NULL DEFAULT now(),"
         "avatar varchar(256) NOT NULL,"
         "email varchar(128) NOT NULL CHECK(length(email)>4),"
         "password varchar(76) NOT NULL,"
         "salt varchar(8) NOT NULL"
         ")"),
    text("CREATE TABLE session ("
         "id bigint generated always as identity primary key,"
         "owner bigint NOT NULL,"
         "token varchar(76) NOT NULL,"
         "created timestamp NOT NULL DEFAULT now(),"
         "CONSTRAINT fk_owner FOREIGN KEY (owner)"
         "REFERENCES users(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE guild ("
         "id bigint generated always as identity primary key,"
         "owner bigint NOT NULL,"
         "creator bigint NOT NULL,"
         "creation_date timestamp NOT NULL DEFAULT now(),"
         "name varchar(50) NOT NULL,"
         "image varchar(256) NOT NULL,"
         "CONSTRAINT fk_owner FOREIGN KEY (owner)"
         "REFERENCES users(id) ON DELETE CASCADE,"
         "CONSTRAINT fk_creator FOREIGN KEY (creator)"
         "REFERENCES users(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE membership_guild("
         "id bigint generated always as identity primary key,"
         "user_id bigint NOT NULL,"
         "guild_id bigint NOT NULL,"
         "joined_at timestamp NOT NULL DEFAULT now(),"
         "CONSTRAINT fk_user_id FOREIGN KEY (user_id)"
         "REFERENCES users(id) ON DELETE CASCADE,"
         "CONSTRAINT fk_guild_id FOREIGN KEY (guild_id)"
         "REFERENCES guild(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE guild_channel("
         "id bigint generated always as identity primary key,"
         "name varchar(100) NOT NULL,"
         "guild bigint NOT NULL,"
         "created timestamp NOT NULL DEFAULT now(),"
         "CONSTRAINT fk_guild FOREIGN KEY (guild)"
         "REFERENCES guild(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE message_on_guild_channel("
         "id bigint generated always as identity primary key,"
         "guild_channel_id bigint NOT NULL,"
         "message varchar(2000) NOT NULL,"
         "sender bigint NOT NULL,"
         "created timestamp NOT NULL DEFAULT now(),"
         "CONSTRAINT fk_guild_channel_id FOREIGN KEY (guild_channel_id)"
         "REFERENCES guild_channel(id) ON DELETE CASCADE,"
         "CONSTRAINT fk_sender FOREIGN KEY (sender)"
         "REFERENCES users(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE channel_group("
         "id bigint generated always as identity primary key,"
         "name varchar(50) NOT NULL,"
         "owner bigint NOT NULL,"
         "registration_date timestamp NOT NULL DEFAULT now(),"
         "image varchar(256) NOT NULL,"
         "type char(1) NOT NULL,"
         "CONSTRAINT fk_owner FOREIGN KEY (owner)"
         "REFERENCES users(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE membership_channel_group("
         "id bigint generated always as identity primary key,"
         "user_id bigint NOT NULL,"
         "channel_group_id bigint NOT NULL,"
         "joined_at timestamp NOT NULL DEFAULT now(),"
         "last_active timestamp NOT NULL DEFAULT now(),"
         "CONSTRAINT fk_user_id FOREIGN KEY (user_id)"
         "REFERENCES users(id) ON DELETE CASCADE,"
         "CONSTRAINT fk_channel_group_id FOREIGN KEY (channel_group_id)"
         "REFERENCES channel_group(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE message_on_channel_group("
         "id bigint generated always as identity primary key,"
         "channel_group_id bigint NOT NULL,"
         "user_id bigint NOT NULL,"
         "message varchar(1000) NOT NULL,"
         "message_time timestamp NOT NULL DEFAULT now(),"
         "CONSTRAINT fk_user_id FOREIGN KEY (user_id)"
         "REFERENCES users(id) ON DELETE CASCADE,"
         "CONSTRAINT fk_channel_group_id FOREIGN KEY (channel_group_id)"
         "REFERENCES channel_group(id) ON DELETE CASCADE"
         ")"),
    text("CREATE TABLE friends("
         "id bigint generated always as identity primary key,"
         "status bigint NOT NULL,"
         "request_sent varchar(200) NOT NULL,"
         "user1 bigint NOT NULL,"
         "user2 bigint NOT NULL,"
         "CONSTRAINT fk_user1 FOREIGN KEY (user1)"
         "REFERENCES users(id) ON DELETE CASCADE,"
         "CONSTRAINT fk_user2 FOREIGN KEY (user2)"
         "REFERENCES users(id) ON DELETE CASCADE"
         ")")
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


