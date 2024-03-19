import abc
from uuid import uuid4

from todo_list.domain.todo_item import TodoItem


class TodoRepository(abc.ABC):

    @abc.abstractmethod
    def get_all(self) -> list[TodoItem]:
        ...

    @abc.abstractmethod
    def get_by_id(self, id: str) -> TodoItem | None:
        ...

    @abc.abstractmethod
    def save(self, todo_item: TodoItem) -> None:
        ...
    
    @abc.abstractmethod
    def delete(self, id: str) -> None:
        ...

    def next_id(self) -> str:
        return uuid4().hex