from functools import lru_cache

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from config import (
    LLMConfig,
    get_executor_config,
    get_planner_config,
    get_reviewer_config,
)


def _build_llm(cfg: LLMConfig) -> BaseChatModel:
    return init_chat_model(
        cfg.model,
        model_provider=cfg.provider,
        api_key=cfg.api_key,
        temperature=cfg.temperature,
    )


@lru_cache
def get_planner_llm() -> BaseChatModel:
    return _build_llm(get_planner_config())


@lru_cache
def get_executor_llm() -> BaseChatModel:
    return _build_llm(get_executor_config())


@lru_cache
def get_reviewer_llm() -> BaseChatModel:
    return _build_llm(get_reviewer_config())
