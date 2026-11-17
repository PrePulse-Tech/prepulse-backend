"""Application configuration loaded from environment variables.

Values are read from real environment variables first, then from a local `.env`
file (never committed - see `.env.example`). All settings are optional for now,
so the app and tests can run without any secrets configured.
"""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # SecretStr hides the value in logs/repr ("**********").
    # Use .get_secret_value() when the real value is needed.
    anthropic_api_key: SecretStr | None = None
    database_url: SecretStr | None = None
    ingest_api_key: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance, so .env is only read once."""
    return Settings()
