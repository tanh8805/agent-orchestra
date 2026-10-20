import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

Role = Literal["planner", "executor", "reviewer"]


@dataclass(frozen=True)
class DatabaseConfig:
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str
    api_key: str
    temperature: float | None = None


@lru_cache
def get_database_config() -> DatabaseConfig:
    return DatabaseConfig(
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        name=os.getenv("POSTGRES_DB", "multi_agent"),
    )


@lru_cache
def get_llm_config(role: Role) -> LLMConfig:
    """Đọc <ROLE>_PROVIDER / _MODEL / _API_KEY / _TEMPERATURE từ .env."""
    prefix = role.upper()
    provider = os.getenv(f"{prefix}_PROVIDER")
    model = os.getenv(f"{prefix}_MODEL")
    api_key = os.getenv(f"{prefix}_API_KEY")
    if not (provider and model and api_key):
        raise ValueError(
            f"Thiếu cấu hình LLM cho {role}: cần {prefix}_PROVIDER, "
            f"{prefix}_MODEL và {prefix}_API_KEY trong .env"
        )

    temperature = os.getenv(f"{prefix}_TEMPERATURE")
    return LLMConfig(
        provider=provider,
        model=model,
        api_key=api_key,
        temperature=float(temperature) if temperature else None,
    )
