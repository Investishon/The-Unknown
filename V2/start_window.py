"""
start_window.py
Стартовый экран
"""

import arcade
import arcade.gui
from constants import *


class StartWindow(arcade.View):
    """Стартовое окно"""

    def __init__(self):
        super().__init__()
        # Менеджер UI (пока не включаем!)
        self.ui_manager = arcade.gui.UIManager()
        self.create_buttons()

    def create_buttons(self):
        """Создаем кнопки"""
        # Вертикальный контейнер
        v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        # Заголовок
        title = arcade.gui.UILabel(
            text="МОЯ ИГРА",
            font_size=36,
            font_name="Arial",
            text_color=TEXT_COLOR,
            bold=True
        )
        v_box.add(title.with_padding(bottom=50))

        # Кнопка "Начать"
        start_btn = arcade.gui.UIFlatButton(
            text="Начать",
            width=200,
            height=50
        )
        start_btn.on_click = self.start_game
        v_box.add(start_btn)

        # Кнопка "Выход"
        exit_btn = arcade.gui.UIFlatButton(
            text="Выход",
            width=200,
            height=50
        )
        exit_btn.on_click = self.exit_game
        v_box.add(exit_btn)

        # Центрируем контейнер
        self.ui_manager.add(arcade.gui.UIAnchorLayout(
            anchor_x="center",
            anchor_y="center",
            child=v_box
        ))

    def start_game(self, event):
        """Начинаем игру"""
        from level_select import LevelSelectWindow
        levels = LevelSelectWindow()
        self.window.show_view(levels)

    def exit_game(self, event):
        """Выход из игры"""
        arcade.exit()

    def on_draw(self):
        """Рисуем экран - ВАЖЕН ПОРЯДОК!"""
        # 1. Очищаем и заливаем фон
        self.clear(BACKGROUND_COLOR)

        # 2. Текст подсказки
        arcade.draw_text(
            "Нажми 'Начать' чтобы выбрать уровень",
            SCREEN_WIDTH // 2, 100,
            TEXT_COLOR, 16,
            anchor_x="center"
        )

        # 3. Кнопки рисуем ПОСЛЕДНИМИ (они будут сверху)
        self.ui_manager.draw()

    def on_show_view(self):
        """Активируем UI при показе окна"""
        self.ui_manager.enable()

    def on_hide_view(self):
        """Деактивируем UI при скрытии окна"""
        self.ui_manager.disable()