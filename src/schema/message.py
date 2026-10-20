from itertools import count
from typing import Literal, TypedDict

Agent = Literal["planner", "executor", "reviewer"]
MessageType = Literal[
    "task_assigned",
    "task_result",
    "review_approved",
    "review_rejected",
    "plan_finished",
]


class Message(TypedDict):
    id: int
    sender: Agent
    recipient: Agent
    type: MessageType
    task_id: int | None
    content: str


_message_ids = count(1)


def new_message(
    sender: Agent, recipient: Agent, type: MessageType, task_id: int | None, content: str
) -> Message:
    return Message(
        id=next(_message_ids),
        sender=sender,
        recipient=recipient,
        type=type,
        task_id=task_id,
        content=content,
    )
