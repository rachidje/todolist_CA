from todo_list.domain.exceptions.todo_exceptions import TodoItemNotDoneError, TodoItemNotFoundError
from todo_list.usecases.todo_usecase import CreateTodoUseCase, DeleteTodoUseCase, ToggleDoneUseCase
from todo_list.domain.todo_item import TodoItem
from tests.fixtures.todo_fixtures import repository, create_todo_item, create_done_todo_item

import pytest


def test_create_new_item(repository): 
    create_todo_item = CreateTodoUseCase(repository)
    created_todo_item = create_todo_item("A New Todo")

    fetched_todo_item = repository.get_by_id(created_todo_item.id)

    assert fetched_todo_item.title == "A New Todo"

def test_toggle_done(repository, create_todo_item):
    assert not create_todo_item.done
    toggle_done = ToggleDoneUseCase(repository)
    toggle_done(create_todo_item)

    todo_item = repository.get_by_id(create_todo_item.id)
    assert todo_item.done

def test_cant_toggle_done_item_not_found(repository):
    toggle_done = ToggleDoneUseCase(repository)
    with pytest.raises(TodoItemNotFoundError):
        toggle_done(TodoItem(id="123", title="A Todo"))

def test_cant_delete_item_not_found(repository):
    delete_item = DeleteTodoUseCase(repository)
    with pytest.raises(TodoItemNotFoundError):
        delete_item(TodoItem(id="123", title="A Todo"))

def test_cant_delete_item_not_done(repository, create_todo_item):
    delete_item = DeleteTodoUseCase(repository)
    with pytest.raises(TodoItemNotDoneError):
        delete_item(create_todo_item)

def test_delete_todo_item(repository, create_done_todo_item):
    delete_item = DeleteTodoUseCase(repository)
    delete_item(create_done_todo_item)

    assert repository.get_by_id(create_done_todo_item.id) == None