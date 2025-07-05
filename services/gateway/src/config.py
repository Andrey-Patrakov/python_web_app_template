from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    GATEWAY_TIMEOUT: int = 59
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
