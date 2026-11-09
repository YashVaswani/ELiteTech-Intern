from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Calorie Tracker API"
    environment: str = "development"

    database_url: str = "sqlite:///./calorie_tracker.db"

    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    cors_origins: list[str] = ["http://localhost:5173"]

    ml_model_id: str = "nateraw/food"
    ml_top_k: int = 3
    max_upload_mb: int = 8
    default_serving_grams: float = 150.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
