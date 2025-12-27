import arcade


class StartWindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.title = None
        self.btn1 = None
        self.btn2 = None
        self.btn3 = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        # Создаём текстовые объекты ОДИН РАЗ
        self.title = arcade.Text("The Unknown", 400, 500, arcade.color.WHITE, 48, anchor_x="center",
                                 font_name="Kenney Future")
        self.btn1 = arcade.Text("Новая игра", 400, 350, arcade.color.WHITE, 24, anchor_x="center",
                                font_name="Kenney Future")
        self.btn2 = arcade.Text("Продолжить", 400, 300, arcade.color.WHITE, 24, anchor_x="center",
                                font_name="Kenney Future")
        self.btn3 = arcade.Text("Авторы", 400, 250, arcade.color.WHITE, 24, anchor_x="center",
                                font_name="Kenney Future")

    def on_draw(self):
        self.clear()
        self.title.draw()
        self.btn1.draw()
        self.btn2.draw()
        self.btn3.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if 300 <= x <= 500:
            if 338 <= y <= 372:  # "Новая игра"
                from level_select import LevelSelect
                self.window.show_view(LevelSelect())
            elif 288 <= y <= 322:  # "Продолжить" - ОТКРЫВАЕМ DORS_WINDOW
                self.open_dors_window()  # ← ВЫЗЫВАЕМ НОВЫЙ МЕТОД
            elif 238 <= y <= 272:  # "Авторы"
                from authors_window import AuthorsWindow
                self.window.show_view(AuthorsWindow())

    def open_dors_window(self):
        """Открывает окно выбора дверей (старую игру) из PyFile"""
        # Закрываем текущее окно меню
        self.window.close()

        import time
        time.sleep(0.1)

        try:
            # Импортируем DorsWindow из PyFile
            import sys
            import os

            # Получаем путь к PyFile
            current_dir = os.path.dirname(os.path.abspath(__file__))  # V2/
            parent_dir = os.path.dirname(current_dir)  # V5/
            pyfile_path = os.path.join(parent_dir, "PyFile")

            # Добавляем PyFile в путь для импорта
            sys.path.insert(0, pyfile_path)

            # Теперь импортируем
            from Dors_window import DorsWindow

            # Запускаем игру
            print("Запускаю DorsWindow...")
            window = DorsWindow()
            arcade.run()

        except ImportError as e:
            print(f"Ошибка загрузки Dors_window: {e}")
            print("Создаю новое окно меню...")

            # Возвращаемся в меню
            new_window = arcade.Window(800, 600, "The Unknown")
            new_window.show_view(StartWindow())
            arcade.run()