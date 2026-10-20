from operator import add, or_
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Send

from graph.executor import executor
from graph.planner import planner
from graph.reviewer import reviewer
from schema import Message, Task, new_message


class State(TypedDict):
    goal: str
    tasks: Annotated[dict[str, Task], or_]  
    messages: Annotated[list[Message], add]


def plan_node(state: State) -> dict:
    tasks = planner(state["goal"])
    message = new_message("planner", "executor", "task_assigned", None, f"{len(tasks)} task")
    return {"tasks": {str(t["id"]): t for t in tasks}, "messages": [message]}


def router(state: State) -> list[Send] | str:
    message = state["messages"][-1]

    if message["recipient"] == "planner":
        return "finish"

    if message["task_id"] is None:
        tasks = list(state["tasks"].values())
    else:
        tasks = [state["tasks"][str(message["task_id"])]]

    if not tasks:
        return "finish"
    return [Send(message["recipient"], t) for t in tasks]


def finish(state: State) -> dict:
    if any(t["status"] == "pending" for t in state["tasks"].values()):
        return {}

    message = new_message("reviewer", "planner", "plan_finished", None, "Tất cả task đã xong")
    return {"messages": [message]}


def build_graph() -> CompiledStateGraph:
    builder = StateGraph(State)
    builder.add_node("planner", plan_node)
    builder.add_node("executor", executor)
    builder.add_node("reviewer", reviewer)
    builder.add_node("finish", finish)

    builder.add_edge(START, "planner")
    for agent in ("planner", "executor", "reviewer"):
        builder.add_conditional_edges(agent, router, ["executor", "reviewer", "finish"])
    builder.add_edge("finish", END)
    return builder.compile()
