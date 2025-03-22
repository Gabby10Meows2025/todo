
from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.utils import colormap

from todo.database import Database

APP_COLOR = colormap['steelblue']
YELLOW     = (1.0, 0.85, 0, 1.0)
LIGHT_TEAL = (0, 0.41, 0.41, 1.0)


class MainWindow(FloatLayout):

    def __init__(self, db: Database, **kwargs):

        super().__init__(**kwargs)

        self.db: Database = db

        todo_list_container: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint=[.85, None],
            height=350,
            pos_hint={"center_x": 0.5, "top": 0.85},
            spacing=10
        )
        title_label: Label = Label(
            font_size=35,
            text="[b]Todo App[/b]",
            size_hint=[1, None],
            markup=True,
        )

        self.inputFrame:     InputFrame     = InputFrame(self)
        self.scrollablelist: ScrollableList = ScrollableList()

        self.todoItems = self.scrollablelist.todoItems

        todo_list_container.add_widget(title_label)
        todo_list_container.add_widget(self.inputFrame)
        todo_list_container.add_widget(self.scrollablelist)

        self.add_widget(todo_list_container)

    def add_todo_item(self, todo_item):
        if todo_item.isspace() or todo_item == "":
            return
        self.db.add_todo_item(todo_item)
        self.todoItems.clear_widgets()
        self.show_existing_items()
        self.inputFrame.todo_input_widget.text = ""

    def delete_todo_item(self, item_id):

        for item in self.todoItems.children:

            if item.item_id == item_id:
                self.db.delete_todo_item(item_id)
                item.parent.remove_widget(item)

    def mark_as_done(self, item_id):

        for item in self.todoItems.children:
            if item.item_id == item_id:
                self.db.mark_as_done(item_id)
                item.mark_done_button.disabled = True

    def show_existing_items(self):
        items = self.db.retrieve_all_items()
        for item in reversed(items):
            item_id, todo_item, done = item
            item = Item(self, item_id, todo_item, done)
            self.todoItems.add_widget(item)


class NoBackgroundButton(Button):
    background_down = ""
    background_normal = ""
    background_disabled = ""


class YellowButton(NoBackgroundButton):
    background_color = YELLOW
    color = APP_COLOR


class LightTealButton(NoBackgroundButton):
    background_color = LIGHT_TEAL


class InputFrame(BoxLayout):
    spacing: int = 8
    height:  int = 45
    size_hint_y = None

    def __init__(self, main_window, **kwargs):

        super().__init__(**kwargs)

        self.todo_input_widget: Input = Input(
            hint_text="Enter a todo activity",
            font_size=22
        )
        self.todo_input_widget.padding = [10, 10, 10, 10]

        add_item_button: YellowButton = YellowButton(
            width=self.height,
            size_hint=[None, 1], text="+"
        )
        add_item_button.bind(
            on_release=lambda *args: main_window.add_todo_item(
                self.todo_input_widget.text
            )
        )

        self.add_widget(self.todo_input_widget)
        self.add_widget(add_item_button)


class ScrollableList(ScrollView):

    effect_cls = ScrollEffect

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.height: int = 400

        self.todoItems: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=14
        )
        self.todoItems.bind(children=self.adjust_height)
        self.add_widget(self.todoItems)

    def adjust_height(self, *args):

        ITEM_HEIGHT: int = 40
        SPACING:     int = 14

        self.todoItems.height = (ITEM_HEIGHT + SPACING) * (
            len(self.todoItems.children)
        ) - SPACING


class Input(TextInput):

    max_length = 65
    multiline = False

    def insert_text(self, *args):
        if len(self.text) < self.max_length:
            super().insert_text(*args)


class Item(BoxLayout):
    size_hint = [1, None]
    spacing = 5

    def __init__(self, main_window: MainWindow, item_id, todo_item, done=False, **kwargs):

        super().__init__(**kwargs)

        self.height:  int = 40
        self.item_id: int = item_id

        item_display_box = LightTealButton(text=todo_item, size_hint=[0.6, 1])

        self.mark_done_button = YellowButton(
            text="Done", size_hint=[None, 1], width=100, disabled=done
        )

        self.mark_done_button.bind(
            on_release=lambda *args: main_window.mark_as_done(item_id)
        )

        remove_button = YellowButton(
            text="-",
            size_hint=[None, 1],
            width=40
        )

        remove_button.bind(
            on_release=lambda *args: main_window.delete_todo_item(item_id)
        )

        self.add_widget(item_display_box)
        self.add_widget(self.mark_done_button)
        self.add_widget(remove_button)
