from typing import List

import dj_database_url
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    SECRET_KEY: str
    WEBHOOK_URL: str
    DEBUG: bool = True
    DATABASE_PUBLIC_URL: str = "sqlite:///db.sqlite3"
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

    @property
    def DB_URL(self) -> str:
        return self.DATABASE_PUBLIC_URL

    @property
    def DATABASES(self):
        """Django DATABASES sozlamasi"""
        return {
            'default': dj_database_url.config(
                default=self.DB_URL,
                conn_max_age=600,
                ssl_require=False
            )
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()

envSettings = get_settings()
