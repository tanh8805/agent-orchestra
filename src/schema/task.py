from typing import Literal, TypedDict

class Task(TypedDict):
    id: int
    description: str
    criteria: str  
    status: Literal["pending", "done", "failed"]
    attempts: int  
    result: str  
    feedback: str  


class Plan(TypedDict):
    goal: str
    tasks: list[Task]
