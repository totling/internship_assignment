import os

from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MONGO_URI = str
    MONGO_DATABASE = str

    KAFKA_SERVER = str
    TOPIC_NAME = str

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

        @classmethod
        def load_env(cls):
            load_dotenv(cls.env_file)


settings = Config()
