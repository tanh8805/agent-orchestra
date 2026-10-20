import os
from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

load_dotenv()

Role = Literal["planner", "executor", "reviewer"]


def _env(role: Role, name: str) -> str | None:
    return os.getenv(f"{role.upper()}_{name}") or None


@lru_cache
def get_llm(role: Role) -> BaseChatModel:
    """Tạo LLM cho một role từ biến môi trường <ROLE>_PROVIDER / _MODEL / _API_KEY / _TEMPERATURE."""
    provider = _env(role, "PROVIDER")
    model = _env(role, "MODEL")
    api_key = _env(role, "API_KEY")
    if not (provider and model and api_key):
        raise ValueError(
            f"Thiếu cấu hình LLM cho {role}: cần {role.upper()}_PROVIDER, "
            f"{role.upper()}_MODEL và {role.upper()}_API_KEY trong .env"
        )

    temperature = _env(role, "TEMPERATURE")
    return init_chat_model(
        model,
        model_provider=provider,
        api_key=api_key,
        temperature=float(temperature) if temperature else None,
    )


def get_planner_llm() -> BaseChatModel:
    return get_llm("planner")


def get_executor_llm() -> BaseChatModel:
    return get_llm("executor")


def get_reviewer_llm() -> BaseChatModel:
    return get_llm("reviewer")
