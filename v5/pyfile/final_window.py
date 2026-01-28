import arcade


class FinalWindow(arcade.View):
    def __init__(self, result="victory", score=0, levels_completed=0, total_levels=3):
        super().__init__()
        self.result = result  # "victory" или "defeat"
        self.score = score  # Очки уже из файла
        self.levels_completed = levels_completed
        self.total_levels = total_levels
        self.title = None
        self.result_text = None
        self.score_text = None
        self.levels_text = None
        self.finish_button = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        # Заголовок
        self.title = arcade.Text(
            "ИГРА ЗАВЕРШЕНА",
            400, 550,
            arcade.color.WHITE, 36,
            anchor_x="center", font_name="Kenney Future"
        )

        # Результат (Победа/Поражение)
        result_color = arcade.color.GOLD if self.result == "victory" else arcade.color.RED
        result_message = "ПОБЕДА!" if self.result == "victory" else "ПОРАЖЕНИЕ"

        self.result_text = arcade.Text(
            result_message,
            400, 450,
            result_color, 48,
            anchor_x="center", font_name="Kenney Future",
            bold=True
        )

        # Статистика
        self.levels_text = arcade.Text(
            f"Пройдено уровней: {self.levels_completed}/{self.total_levels}",
            400, 350,
            arcade.color.LIGHT_BLUE, 24,
            anchor_x="center", font_name="Kenney Future"
        )

        self.score_text = arcade.Text(
            f"Финальные очки: {self.score}",
            400, 300,
            arcade.color.LIGHT_GREEN, 24,
            anchor_x="center", font_name="Kenney Future"
        )

        # Кнопка завершения
        self.finish_button = arcade.Text(
            "Завершить",
            400, 200,
            arcade.color.WHITE, 28,
            anchor_x="center", font_name="Kenney Future"
        )

    def on_draw(self):
        self.clear()
        self.title.draw()
        self.result_text.draw()
        self.levels_text.draw()
        self.score_text.draw()
        self.finish_button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Нажатие на кнопку "Завершить"
        if 325 <= x <= 475 and 188 <= y <= 212:
            self.return_to_main_menu()

    def return_to_main_menu(self):
        try:
            from start_window import StartWindow
            start_view = StartWindow()
            self.window.show_view(start_view)
        except ImportError:
            self.window.close()
