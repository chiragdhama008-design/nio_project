"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Supabase
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None

    # AI provider
    ai_api_key: Optional[str] = None
    ai_provider: str = "fallback"
    ai_model: str = "openai/gpt-oss-120b"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def has_supabase(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)

    @property
    def has_ai(self) -> bool:
        return bool(self.ai_api_key) and self.ai_provider != "fallback"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
