from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_model: str = "anthropic/claude-sonnet-4-5"
    supabase_url: str = ""
    supabase_key: str = ""
    news_api_key: str = ""
    mlflow_tracking_uri: str = "http://mlflow:5000"
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
