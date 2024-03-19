import pytest

from todo_list.infrastructure.repositories.in_memory_todo_repository import InMemoryTodoRepository
from todo_list.usecases.todo_usecase import CreateTodoUseCase, ToggleDoneUseCase

@pytest.fixture
def repository():
    return InMemoryTodoRepository()

@pytest.fixture
def create_todo_item(repository):
    create_todo_item = CreateTodoUseCase(repository)
    return create_todo_item("A New Todo")

@pytest.fixture
def create_done_todo_item(repository):
    create_todo_item = CreateTodoUseCase(repository)
    todo_item = create_todo_item("A New Todo")

    toggle_done = ToggleDoneUseCase(repository)
    toggle_done(todo_item)

    return todo_item