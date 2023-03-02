import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "postgres")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASS = os.environ.get("DB_PASS", "postgres")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
