from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    #MODE: Literal["DEV", "TEST", "PROD"]
    #LOG_LEVEL: str
    #SENTRY_URL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SMTP_HOST : str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    @property
    def DATABASE_URL(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:'
                f'{self.DB_PASS}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')

    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()
