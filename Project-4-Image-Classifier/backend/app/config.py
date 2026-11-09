from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    cors_origins: list[str] = ["http://localhost:5173"]
    max_upload_bytes: int = 5 * 1024 * 1024


settings = Settings()
