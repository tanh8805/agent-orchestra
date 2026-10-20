from functools import lru_cache

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from config import Role, get_llm_config


@lru_cache
def get_llm(role: Role) -> BaseChatModel:
    cfg = get_llm_config(role)
    return init_chat_model(
        cfg.model,
        model_provider=cfg.provider,
        api_key=cfg.api_key,
        temperature=cfg.temperature,
    )


def get_planner_llm() -> BaseChatModel:
    return get_llm("planner")


def get_executor_llm() -> BaseChatModel:
    return get_llm("executor")


def get_reviewer_llm() -> BaseChatModel:
    return get_llm("reviewer")
