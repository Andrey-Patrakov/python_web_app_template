import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', '.env'))


settings = Settings()


def get_db_url():
    url = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}'
    url += f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
    return url
