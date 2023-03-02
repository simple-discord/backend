from sqlalchemy import create_engine

from sql_app.config import get_settings

query = "CREATE TABLE user (" \
        "id bigint generated always as identity primary key," \
        "username varchar(50) NOT NULL," \
        "registration_date timestamp NOT NULL now()," \
        "avatar varchar(256) NOT NULL," \
        "email varchar(128) NOT NULL CHECK(length(email)>4)," \
        "password varchar(76) NOT NULL," \
        "salt varchar(8) NOT NULL" \
        ")"

s = get_settings()

engine = create_engine(f'postgresql://{s.DB_USER}:{s.DB_PASS}@{s.DB_HOST}/{s.DB_NAME}')
with engine.connect() as con:
   con.execute(query)
   con.commit()
