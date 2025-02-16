import logging

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base import Base


class DatabaseSettings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    CONNECTION_STRING: str
    FUEL_IX_API_KEY: str
    NEWS_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


__ENV_SETTINGS__ = DatabaseSettings()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class Database:
    def __init__(self):
        self.engine = create_engine(
            __ENV_SETTINGS__.CONNECTION_STRING,
            echo=True,
        )

    def get_session(self):
        session_factory = sessionmaker(bind=self.engine)
        Session = scoped_session(session_factory)
        return Session()
