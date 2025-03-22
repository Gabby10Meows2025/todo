
from kivy.app import App

from kivy.core.window import Window

from todo.widgets import MainWindow
from todo.widgets import APP_COLOR


from todo.database import Database

Window.clearcolor = APP_COLOR


class TodoApp(App):
    title = "Todo App"

    def build(self):
        return MainWindow(db=Database())


if __name__ == "__main__":
    todoapp = TodoApp()
    todoapp.run()