from typing import List

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str

    SECRET_KEY: str
    WEBHOOK_URL: str
    DEBUG: bool = True

    MY_VERIFY: str
    SHORT_TIME_ACCESS_TOKEN: str
    CLIENT_ID: int
    CLIENT_SECRET: str
    GENERATE_TOKEN_WEBHOOK: str
    LONG_TIME_TOKEN: str
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672//"

    @property
    def ALLOWED_HOSTS(self) -> List[str]:
        return [
            "127.0.0.1",
            "localhost",
            "0.0.0.0",
            self.WEBHOOK_URL,
        ]

    class Config:
        env_file = ".env"



@lru_cache
def get_settings() -> Settings:
    return Settings()

envSettings = get_settings()
