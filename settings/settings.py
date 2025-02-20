import logging

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base import Base
import boto3



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
    S3_BUCKET_NAME: str

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


class s3ClientHelper:
    def __init__(self):
        self.s3_client = boto3.client(
            service_name='s3',
            aws_access_key_id=__ENV_SETTINGS__.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=__ENV_SETTINGS__.AWS_SECRET_ACCESS_KEY
            )

    def get_s3_client(self):
        return self.s3_client

    def save_file_to_s3(self, file, file_path, bucket_name=__ENV_SETTINGS__.S3_BUCKET_NAME):
        self.s3_client.put_object(Body=file, Bucket=bucket_name, Key=file_path)

    def get_file_from_s3(self, file_path, bucket_name=__ENV_SETTINGS__.S3_BUCKET_NAME):
        return self.s3_client.get_object(Bucket=bucket_name, Key=file_path)
