from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsDB(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_')

    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASSWORD: str


class SettingsStorage(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='STORAGE_')

    URL: str
    BUCKET: str
    ACCESS_KEY: str
    SECRET_KEY: str


class SettingsSMTP(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SMTP_')

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    SSL_REQUIRED: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    db: SettingsDB = SettingsDB()
    storage: SettingsStorage = SettingsStorage()
    smtp: SettingsSMTP = SettingsSMTP()

    REGION_NAME: str = 'ru-moscow'
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    BACKEND_URL: str
    FRONTEND_URL: str


settings = Settings()


def get_db_url():
    url = f'postgresql+asyncpg://{settings.db.USER}:{settings.db.PASSWORD}'
    url += f'@{settings.db.HOST}:{settings.db.PORT}/{settings.db.NAME}'
    return url
