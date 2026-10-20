from llm.llm import get_executor_llm
from schema import Task, new_message


def executor(state: Task) -> dict:
    task = state.copy()
    prompt = (
        "Bạn là Executor. Thực hiện task sau và báo cáo kết quả.\n\n"
        f"Task: {task['description']}\n"
        f"Tiêu chí hoàn thành: {task['criteria']}"
    )
    if task["feedback"]:
        prompt += f"\n\nLần trước bị Reviewer từ chối: {task['feedback']}\nHãy làm lại."

    task["result"] = get_executor_llm().invoke(prompt).text

    message = new_message("executor", "reviewer", "task_result", task["id"], task["result"])
    return {"tasks": {str(task["id"]): task}, "messages": [message]}
