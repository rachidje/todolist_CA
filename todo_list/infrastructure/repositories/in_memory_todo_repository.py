from todo_list.domain.todo_item import TodoItem
from todo_list.domain.todo_repository import TodoRepository


class InMemoryTodoRepository(TodoRepository):
    def __init__(self):
        self._items = {}

    def get_all(self) -> list[TodoItem]:
        return list(self._items.values())
    
    def get_by_id(self, id: str) -> TodoItem | None:
        try:
            return self._items[id]
        except KeyError:
            return None
    
    def save(self, todo_item : TodoItem) -> None:
        self._items[todo_item.id] = todo_item

    def delete(self, id: str) -> None:
        del self._items[id]