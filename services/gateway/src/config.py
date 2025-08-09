from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    GATEWAY_TIMEOUT: int = 59
    REGION_NAME: str = 'ru-moscow'
    SERVICES: dict = {}

    FRONTEND_HOST: str
    FRONTEND_PORT: str
    ALLOWED_HOSTS: list[str] = []

    USERS_SERVICE_PREFIX: str = '/api/users'

    FILE_MAX_LENGTH: int = 256 * 1024**2


settings = Settings()


def get_allowed_hosts():
    allowed_hosts = settings.ALLOWED_HOSTS
    allowed_hosts.append(f'{settings.FRONTEND_HOST}:{settings.FRONTEND_HOST}')
    if settings.FRONTEND_PORT == "80":
        allowed_hosts.append(settings.FRONTEND_HOST)

    return allowed_hosts
