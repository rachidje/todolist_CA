from todo_list.domain.todo_repository import TodoRepository


class UseCase:
    _repo: TodoRepository

    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo