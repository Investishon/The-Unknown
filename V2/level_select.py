"""
level_select.py
Выбор уровня
"""

import arcade
import arcade.gui
from constants import *


class LevelSelectWindow(arcade.View):
    """Окно выбора уровня"""

    def __init__(self):
        super().__init__()


        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()


        self.create_level_buttons()

    def create_level_buttons(self):


        v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=15)


        title = arcade.gui.UILabel(
            text="Выбери уровень",
            font_size=28,
            font_name="Arial",
            text_color=TEXT_COLOR,
            bold=True
        )
        v_box.add(title.with_padding(bottom=30))


        for i, level in enumerate(LEVELS):
            level_btn = arcade.gui.UIFlatButton(
                text=level["name"],
                width=250,
                height=50,
                style={"bg_color": level["color"]}
            )
            level_btn.on_click = lambda event, idx=i: self.select_level(event, idx)
            v_box.add(level_btn)

        back_btn = arcade.gui.UIFlatButton(
            text="Назад",
            width=150,
            height=40
        )
        back_btn.on_click = self.go_back
        v_box.add(back_btn.with_padding(top=30))

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center",
                child=v_box
            )
        )

    def select_level(self, event, level_index):
        level_name = LEVELS[level_index]["name"]
        print(f"Выбран уровень: {level_name}")

        print(f"Уровень {level_name} загружается...")

    def go_back(self, event):
        """Возвращаемся назад"""
        from V2.start_window import StartWindow
        start = StartWindow()
        self.window.show_view(start)

    def on_draw(self):
        self.clear()
        # 1. Кнопки
        self.ui_manager.draw()
        # 2. Текст
        arcade.draw_text("Подсказка...", ...)
        # 3. ФОН В КОНЦЕ
        arcade.draw_rectangle_filled(...)

        self.ui_manager.draw()

        arcade.draw_text(
            "Нажми на уровень чтобы начать",
            SCREEN_WIDTH // 2, 120,
            TEXT_COLOR, 16,
            anchor_x="center"
        )

    def on_show_view(self):
        self.ui_manager.enable()

    def on_hide_view(self):
        self.ui_manager.disable()