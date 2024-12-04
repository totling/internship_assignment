import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MONGO_URI: str
    MONGO_DATABASE: str

    KAFKA_SERVER: str
    TOPIC_NAME: str
    KAFKA_GROUP_ID: str

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env_doc_stor"))

        @classmethod
        def load_env(cls):
            load_dotenv(cls.env_file)


settings = Config()
