from types import SimpleNamespace

import pytest

from schema import Task


class FakeLLM:
    """LLM giả: reply(prompt) trả về nội dung (text) hoặc object có cấu trúc."""

    def __init__(self, reply):
        self.reply = reply

    def invoke(self, prompt):
        return SimpleNamespace(text=self.reply(prompt))

    def with_structured_output(self, schema):
        return SimpleNamespace(invoke=self.reply)


@pytest.fixture
def fake_llm(monkeypatch):
    def install(role: str, reply):
        # Gắn LLM giả vào module của agent tương ứng (planner/executor/reviewer)
        monkeypatch.setattr(f"graph.{role}.get_{role}_llm", lambda: FakeLLM(reply))

    return install


@pytest.fixture
def make_task():
    def make(**overrides) -> Task:
        task = Task(
            id=1,
            description="việc 1",
            criteria="ok",
            status="pending",
            attempts=0,
            result="",
            feedback="",
        )
        task.update(overrides)  # type: ignore[typeddict-item]
        return task

    return make
