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
    FILE_MAX_LENGTH: int = 500 * 1024**2


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

    FRONTEND_HOST: str
    FRONTEND_PORT: str
    ALLOWED_HOSTS: list[str] = []


settings = Settings()


def get_db_url():
    url = f'postgresql+asyncpg://{settings.db.USER}:{settings.db.PASSWORD}'
    url += f'@{settings.db.HOST}:{settings.db.PORT}/{settings.db.NAME}'
    return url


def get_allowed_hosts():
    allowed_hosts = settings.ALLOWED_HOSTS
    allowed_hosts.append(f'{settings.FRONTEND_HOST}:{settings.FRONTEND_HOST}')
    if settings.FRONTEND_PORT == "80":
        allowed_hosts.append(settings.FRONTEND_HOST)

    return allowed_hosts
