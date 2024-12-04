import os

from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    KAFKA_SERVER: str
    TOPIC_NAME: str

    @model_validator(mode="before")
    @classmethod
    def get_database_url(cls, v):
        v["DATABASE_URL"] = (
            f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}"
            f":{v['DB_PORT']}/{v['DB_NAME']}"
        )
        return v

    DATABASE_URL: str = ""

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env_users"))

        @classmethod
        def load_env(cls):
            load_dotenv(cls.env_file)


settings = Config()
