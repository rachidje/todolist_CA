from dataclasses import dataclass

@dataclass
class TodoItem:
    id: str
    title: str
    done: bool = False