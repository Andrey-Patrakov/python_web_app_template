from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsSMTP(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SMTP_')

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    SSL_REQUIRED: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    smtp: SettingsSMTP = SettingsSMTP()

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SECURE: bool = False

    FRONTEND_HOST: str
    FRONTEND_PORT: str
    LINK_EXPIRE_MINUTES: int = 30


settings = Settings()
