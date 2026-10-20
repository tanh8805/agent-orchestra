from typing import cast

from pydantic import BaseModel

from llm.llm import get_reviewer_llm
from schema import Task, new_message

MAX_RETRIES = 2


class Verdict(BaseModel):
    approved: bool
    feedback: str


def reviewer(state: Task) -> dict:
    task = state.copy()
    llm = get_reviewer_llm().with_structured_output(Verdict)
    verdict = cast(
        Verdict,
        llm.invoke(
            "Bạn là Reviewer. Đánh giá kết quả có đạt tiêu chí hay không.\n\n"
            f"Task: {task['description']}\n"
            f"Tiêu chí hoàn thành: {task['criteria']}\n"
            f"Kết quả: {task['result']}"
        ),
    )

    if verdict.approved:
        task["status"] = "done"
        task["feedback"] = ""
        message = new_message("reviewer", "planner", "review_approved", task["id"], "Đạt")
        return {"tasks": {str(task["id"]): task}, "messages": [message]}

    task["feedback"] = verdict.feedback

    if task["attempts"] >= MAX_RETRIES:
        task["status"] = "failed"
        message = new_message("reviewer", "planner", "review_rejected", task["id"], task["feedback"])
        return {"tasks": {str(task["id"]): task}, "messages": [message]}

    # Chưa hết lượt: nhắn lại cho executor làm lại
    task["attempts"] += 1
    message = new_message("reviewer", "executor", "review_rejected", task["id"], task["feedback"])
    return {"tasks": {str(task["id"]): task}, "messages": [message]}
