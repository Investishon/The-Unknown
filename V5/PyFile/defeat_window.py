import arcade


class DefeatWindow(arcade.View):
    def __init__(self, score=0, level=1):
        super().__init__()
        self.score = score
        self.level = level
        self.title = None
        self.score_text = None
        self.level_text = None
        self.restart_button = None
        self.menu_button = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        # Заголовок ПОРАЖЕНИЕ
        self.title = arcade.Text(
            "ПОРАЖЕНИЕ",
            400, 500,
            arcade.color.RED, 48,
            anchor_x="center", font_name="Kenney Future",
            bold=True
        )

        # Причина смерти
        self.death_reason = arcade.Text(
            "Ваш персонаж был побежден",
            400, 420,
            arcade.color.WHITE, 24,
            anchor_x="center", font_name="Kenney Future"
        )

        # Статистика
        self.level_text = arcade.Text(
            f"Достигнут уровень: {self.level}",
            400, 350,
            arcade.color.LIGHT_BLUE, 24,
            anchor_x="center", font_name="Kenney Future"
        )

        self.score_text = arcade.Text(
            f"Накопленные очки: {self.score}",
            400, 300,
            arcade.color.LIGHT_GREEN, 24,
            anchor_x="center", font_name="Kenney Future"
        )

        # Кнопка начать заново
        self.restart_button = arcade.Text(
            "Начать заново",
            400, 200,
            arcade.color.WHITE, 28,
            anchor_x="center", font_name="Kenney Future"
        )

        # Кнопка в главное меню
        self.menu_button = arcade.Text(
            "Главное меню",
            400, 150,
            arcade.color.WHITE, 24,
            anchor_x="center", font_name="Kenney Future"
        )

    def on_draw(self):
        self.clear()
        self.title.draw()
        self.death_reason.draw()
        self.level_text.draw()
        self.score_text.draw()
        self.restart_button.draw()
        self.menu_button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Нажатие на "Начать заново"
        if 325 <= x <= 475 and 188 <= y <= 222:
            self.restart_game()

        # Нажатие на "Главное меню"
        if 325 <= x <= 475 and 138 <= y <= 172:
            self.return_to_main_menu()

    def restart_game(self):
        """Начинает игру заново с уровня 1"""
        try:
            # Очищаем файл с очками при перезапуске
            try:
                with open("coin.txt", "w") as f:
                    f.write("0")
            except:
                pass

            from dors_window import DorsView
            # Начинаем с уровня 1, без сохраненного игрока
            dors = DorsView(level=1, player=None)
            self.window.show_view(dors)
        except ImportError as e:
            self.window.close()

    def return_to_main_menu(self):
        """Возврат в главное меню"""
        try:
            from start_window import StartWindow
            start_view = StartWindow()
            self.window.show_view(start_view)
        except ImportError:
            self.window.close()


