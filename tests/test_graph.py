import re
from collections import Counter

from graph import build_graph
from graph.planner import PlanOutput, TaskSpec
from graph.reviewer import Verdict


def task_number(prompt: str) -> str:
    return re.findall(r"việc (\d)", prompt)[0]


def plan_of(n: int):
    specs = [TaskSpec(description=f"việc {i}", criteria="ok") for i in range(1, n + 1)]
    return lambda prompt: PlanOutput(tasks=specs)


def test_one_executor_per_task(fake_llm):
    runs = Counter()

    def execute(prompt):
        runs[task_number(prompt)] += 1
        return "kết quả"

    fake_llm("planner", plan_of(4))
    fake_llm("executor", execute)
    fake_llm("reviewer", lambda prompt: Verdict(approved=True, feedback=""))

    out = build_graph().invoke({"goal": "g"})

    assert runs == {"1": 1, "2": 1, "3": 1, "4": 1}
    assert [t["status"] for t in out["tasks"].values()] == ["done"] * 4


def test_rejected_task_is_redone_then_fails(fake_llm):
    runs = Counter()

    def execute(prompt):
        runs[task_number(prompt)] += 1
        return f"lần {runs[task_number(prompt)]}"

    def review(prompt):
        # việc 1 luôn đạt, việc 2 đạt ở lần làm lại, việc 3 không bao giờ đạt
        n = task_number(prompt)
        ok = n == "1" or (n == "2" and "lần 2" in prompt)
        return Verdict(approved=ok, feedback="" if ok else "chưa đạt")

    fake_llm("planner", plan_of(3))
    fake_llm("executor", execute)
    fake_llm("reviewer", review)

    out = build_graph().invoke({"goal": "g"})

    assert runs == {"1": 1, "2": 2, "3": 3}
    tasks = out["tasks"].values()
    assert [(t["status"], t["attempts"]) for t in tasks] == [
        ("done", 0),
        ("done", 1),
        ("failed", 2),
    ]


def test_messages_are_logged_and_plan_finished_once(fake_llm):
    fake_llm("planner", plan_of(2))
    fake_llm("executor", lambda prompt: "ok")
    fake_llm("reviewer", lambda prompt: Verdict(approved=True, feedback=""))

    out = build_graph().invoke({"goal": "g"})

    types = Counter(m["type"] for m in out["messages"])
    assert types == {
        "task_assigned": 1,
        "task_result": 2,
        "review_approved": 2,
        "plan_finished": 1,
    }
    ids = [m["id"] for m in out["messages"]]
    assert len(set(ids)) == len(ids)


def test_empty_plan_finishes_without_executor(fake_llm):
    fake_llm("planner", plan_of(0))
    fake_llm("executor", lambda prompt: 1 / 0)
    fake_llm("reviewer", lambda prompt: 1 / 0)

    out = build_graph().invoke({"goal": "g"})

    assert out["tasks"] == {}
