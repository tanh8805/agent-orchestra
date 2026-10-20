import pytest

from config import get_database_config, get_executor_config, get_planner_config


@pytest.fixture(autouse=True)
def clear_cache():
    get_planner_config.cache_clear()
    get_executor_config.cache_clear()
    get_database_config.cache_clear()


def test_llm_config_read_from_env(monkeypatch):
    monkeypatch.setenv("PLANNER_PROVIDER", "openai")
    monkeypatch.setenv("PLANNER_MODEL", "gpt-4o")
    monkeypatch.setenv("PLANNER_API_KEY", "secret")
    monkeypatch.setenv("PLANNER_TEMPERATURE", "0.5")

    cfg = get_planner_config()

    assert (cfg.provider, cfg.model, cfg.api_key, cfg.temperature) == (
        "openai",
        "gpt-4o",
        "secret",
        0.5,
    )


def test_llm_config_temperature_is_optional(monkeypatch):
    monkeypatch.setenv("PLANNER_PROVIDER", "openai")
    monkeypatch.setenv("PLANNER_MODEL", "gpt-4o")
    monkeypatch.setenv("PLANNER_API_KEY", "secret")
    monkeypatch.delenv("PLANNER_TEMPERATURE", raising=False)

    assert get_planner_config().temperature is None


def test_llm_config_missing_api_key_raises(monkeypatch):
    monkeypatch.setenv("EXECUTOR_PROVIDER", "openai")
    monkeypatch.setenv("EXECUTOR_MODEL", "gpt-4o")
    monkeypatch.setenv("EXECUTOR_API_KEY", "")

    with pytest.raises(ValueError, match="EXECUTOR_API_KEY"):
        get_executor_config()


def test_database_url(monkeypatch):
    monkeypatch.setenv("POSTGRES_USER", "u")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p")
    monkeypatch.setenv("POSTGRES_HOST", "db")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    monkeypatch.setenv("POSTGRES_DB", "d")

    url = get_database_config().url

    assert url.render_as_string(hide_password=False) == "postgresql+psycopg://u:p@db:5433/d"
