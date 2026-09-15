from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_provider: Literal["openai", "anthropic"] = "openai"
    llm_model: str = "gpt-4o-mini"

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    app_env: str = "development"
    log_level: str = "info"


@lru_cache
def get_settings() -> Settings:
    return Settings()
