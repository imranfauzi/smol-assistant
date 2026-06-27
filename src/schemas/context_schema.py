from dataclasses import dataclass

@dataclass(frozen=True)
class Context:
    thread_id: str
    user_id: str | None = None