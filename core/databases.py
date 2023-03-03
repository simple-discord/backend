from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_app.config import get_settings


class DiscordDatabaseManager:

    session_factory = None

    @staticmethod
    def init_pool():
        s = get_settings()
        sqlalchemy_database_url = f"postgresql://{s.DB_USER}:{s.DB_PASS}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"

        engine = create_engine(
            sqlalchemy_database_url
        )

        DiscordDatabaseManager.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def get_db_session():
        db = DiscordDatabaseManager.session_factory()
        try:
            yield db
        finally:
            db.close()
