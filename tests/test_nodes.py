from graph.executor import executor
from graph.reviewer import MAX_RETRIES, Verdict, reviewer


def test_executor_saves_result_and_messages_reviewer(fake_llm, make_task):
    fake_llm("executor", lambda prompt: "xong rồi")

    out = executor(make_task())

    assert out["tasks"]["1"]["result"] == "xong rồi"
    message = out["messages"][0]
    assert (message["type"], message["recipient"]) == ("task_result", "reviewer")


def test_executor_prompt_includes_feedback_when_retrying(fake_llm, make_task):
    prompts = []
    fake_llm("executor", lambda prompt: prompts.append(prompt) or "ok")

    executor(make_task(feedback="thiếu ví dụ"))

    assert "thiếu ví dụ" in prompts[0]


def test_reviewer_approves_task(fake_llm, make_task):
    fake_llm("reviewer", lambda prompt: Verdict(approved=True, feedback=""))

    out = reviewer(make_task(result="tốt", feedback="cũ"))

    task = out["tasks"]["1"]
    assert (task["status"], task["feedback"]) == ("done", "")
    message = out["messages"][0]
    assert (message["type"], message["recipient"]) == ("review_approved", "planner")


def test_reviewer_rejects_and_messages_executor(fake_llm, make_task):
    fake_llm("reviewer", lambda prompt: Verdict(approved=False, feedback="sai"))

    out = reviewer(make_task(attempts=0))

    task = out["tasks"]["1"]
    assert (task["status"], task["attempts"], task["feedback"]) == ("pending", 1, "sai")
    message = out["messages"][0]
    assert (message["type"], message["recipient"]) == ("review_rejected", "executor")


def test_reviewer_fails_task_after_max_retries(fake_llm, make_task):
    fake_llm("reviewer", lambda prompt: Verdict(approved=False, feedback="sai"))

    out = reviewer(make_task(attempts=MAX_RETRIES))

    task = out["tasks"]["1"]
    assert (task["status"], task["attempts"]) == ("failed", MAX_RETRIES)
    assert out["messages"][0]["recipient"] == "planner"
