from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsStorage(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='STORAGE_')

    URL: str
    BUCKET: str
    ACCESS_KEY: str
    SECRET_KEY: str
    FILE_MAX_LENGTH: int = 256 * 1024**2
    CHUNK_SIZE: int = 524288


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    storage: SettingsStorage = SettingsStorage()

    GATEWAY_TIMEOUT: int = 59
    REGION_NAME: str = 'ru-moscow'
    SERVICES: dict = {}

    FRONTEND_HOST: str
    FRONTEND_PORT: str
    ALLOWED_HOSTS: list[str] = []


settings = Settings()


def get_allowed_hosts():
    allowed_hosts = settings.ALLOWED_HOSTS
    allowed_hosts.append(f'{settings.FRONTEND_HOST}:{settings.FRONTEND_HOST}')
    if settings.FRONTEND_PORT == "80":
        allowed_hosts.append(settings.FRONTEND_HOST)

    return allowed_hosts
