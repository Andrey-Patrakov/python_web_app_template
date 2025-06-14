from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    GATEWAY_TIMEOUT: int = 59
    SERVICES: dict = {}


settings = Settings()
