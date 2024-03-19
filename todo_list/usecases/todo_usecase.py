from todo_list.domain.exceptions.todo_exceptions import TodoItemNotDoneError, TodoItemNotFoundError
from todo_list.domain.todo_item import TodoItem
from todo_list.usecases.usecase import UseCase


class CreateTodoUseCase(UseCase):
    def __call__(self, title: str) -> TodoItem:
        todo_item = TodoItem(id= self._repo.next_id(), title=title)
        self._repo.save(todo_item)
        return todo_item

class ToggleDoneUseCase(UseCase):
    def __call__(self, todo_item: TodoItem) -> None:
        if not self._repo.get_by_id(todo_item.id):
            raise TodoItemNotFoundError
        todo_item.done = not todo_item.done
        self._repo.save(todo_item)

class DeleteTodoUseCase(UseCase):
    def __call__(self, todo_item: TodoItem) -> None:
        if not self._repo.get_by_id(todo_item.id):
            raise TodoItemNotFoundError
        if not todo_item.done:
            raise TodoItemNotDoneError
        self._repo.delete(todo_item.id)