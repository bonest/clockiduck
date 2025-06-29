from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from .env file and environment variables."""

    CLOCKIFY_API_KEY: str
    CLOCKIFY_WORKSPACE_ID: str
    ROUNDING_MINUTES: int = 15
    DAY_START_TIME: str = "08:00"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()