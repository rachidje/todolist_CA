import os, sys
sys.path.append(os.getcwd())

from todo_list.domain.exceptions.todo_exceptions import TodoItemNotDoneError
from todo_list.domain.todo_item import TodoItem

from venv import create
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup


from todo_list.infrastructure.repositories.in_memory_todo_repository import InMemoryTodoRepository
from todo_list.usecases.todo_usecase import CreateTodoUseCase, DeleteTodoUseCase, ToggleDoneUseCase

repo = InMemoryTodoRepository()
create_todo_usecase = CreateTodoUseCase(repo)
toggle_todo_usecase = ToggleDoneUseCase(repo)
delete_todo_usecase = DeleteTodoUseCase(repo)


class ErrorPopup(Popup):
    def __init__(self, error_message, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.title = 'Error'
        self.content = Label(text=error_message)
        self.size_hint = (None, None)
        self.size = (300, 200)

class TodoItemBox(BoxLayout):
    def __init__(self, todo_item: TodoItem, **kwargs):
        self.entity = todo_item
        super(TodoItemBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        self.label = Label(text= self.entity.title)
        if self.entity.done:
            self.label.color = (0.5, 0.5, 0.5, 1)  # Gray color for done items
        self.add_widget(self.label)

        self.toggle_button = Button(text='Done' if not self.entity.done else 'Undone')
        self.toggle_button.bind(on_press=self.toggle_done)
        self.add_widget(self.toggle_button)

        self.delete_button = Button(text='Delete')
        self.delete_button.bind(on_press=self.delete_item)
        self.add_widget(self.delete_button)

    def toggle_done(self, instance):
        toggle_todo_usecase(self.entity)
        self.label.color = (0.5, 0.5, 0.5, 1) if self.entity.done else (1, 1, 1, 1)
        self.toggle_button.text = 'Done' if not self.entity.done else 'Undone'

    def delete_item(self, instance):
        try:
            delete_todo_usecase(self.entity)
            self.parent.remove_widget(self)
        except TodoItemNotDoneError:
            error_popup = ErrorPopup('You can only delete done items')
            error_popup.open()


class TodoListApp(App):
    def build(self):
        self.todo_repository = repo

        # Layout
        layout = BoxLayout(orientation='vertical')

        # Text Input
        self.text_input = TextInput(hint_text='Enter a new item', multiline=False)
        layout.add_widget(self.text_input)

        # Add Button
        add_button = Button(text='Add Item')
        add_button.bind(on_press=self.add_item)
        layout.add_widget(add_button)

        # Delete All Done Button
        delete_all_done_button = Button(text='Delete All Done')
        delete_all_done_button.bind(on_press=self.delete_all_done)
        layout.add_widget(delete_all_done_button)

        # Scroll View
        self.scroll_view = BoxLayout(orientation='vertical')
        layout.add_widget(self.scroll_view)

        return layout

    def add_item(self, instance):
        text = self.text_input.text.strip()
        if text:
            entity = create_todo_usecase(title= text)
            self.scroll_view.add_widget(TodoItemBox(entity))

            self.text_input.text = ''

    def delete_all_done(self, instance):
        for entity in self.todo_repository.get_all():
            if entity.done:
                delete_todo_usecase(entity)
                self.scroll_view.remove_widget(TodoItemBox(entity))
        self.update_display()

    def update_display(self):
        # Clear previous display
        self.scroll_view.clear_widgets()

        # Rebuild display
        for entity in self.todo_repository.get_all():
            todo_item_box = TodoItemBox(todo_item=entity)
            self.scroll_view.add_widget(todo_item_box)


if __name__ == '__main__':
    TodoListApp().run()
