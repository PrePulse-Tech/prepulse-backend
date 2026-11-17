import pytest

from app.config import Settings

ENV_VARS = ("ANTHROPIC_API_KEY", "DATABASE_URL", "INGEST_API_KEY")


def test_settings_load_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/test")
    monkeypatch.setenv("INGEST_API_KEY", "test-ingest-key")

    settings = Settings(_env_file=None)  # ignore any local .env file

    assert settings.anthropic_api_key.get_secret_value() == "test-anthropic-key"
    assert settings.database_url.get_secret_value() == "postgresql://user:pass@localhost:5432/test"
    assert settings.ingest_api_key.get_secret_value() == "test-ingest-key"


def test_settings_are_optional(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)

    settings = Settings(_env_file=None)

    assert settings.anthropic_api_key is None
    assert settings.database_url is None
    assert settings.ingest_api_key is None


def test_secrets_are_hidden_in_repr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")

    settings = Settings(_env_file=None)

    assert "test-anthropic-key" not in repr(settings)
