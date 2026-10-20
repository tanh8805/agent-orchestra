from typing import cast

from pydantic import BaseModel

from llm.llm import get_planner_llm
from schema import Task


class TaskSpec(BaseModel):
    description: str
    criteria: str


class PlanOutput(BaseModel):
    tasks: list[TaskSpec]


def planner(goal: str) -> list[Task]:
    llm = get_planner_llm().with_structured_output(PlanOutput)
    output = cast(
        PlanOutput,
        llm.invoke(
            "Bạn là Planner. Chia mục tiêu sau thành các task nhỏ, độc lập với nhau, "
            "mỗi task có tiêu chí hoàn thành rõ ràng.\n\n"
            f"Mục tiêu: {goal}"
        ),
    )

    return [
        Task(
            id=i,
            description=spec.description,
            criteria=spec.criteria,
            status="pending",
            attempts=0,
            result="",
            feedback="",
        )
        for i, spec in enumerate(output.tasks, start=1)
    ]
