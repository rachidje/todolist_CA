
class TodoItemNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Todo item not found")

class TodoItemNotDoneError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Todo item is not done")