from dataclasses import dataclass
from dataclasses import field

@dataclass
class Task:
    task_id: str
    prompt: str
    categories: list[str] = field(default_factory=list)
    complexity: str | None = None
