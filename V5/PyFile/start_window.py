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
        self.btn2 = arcade.Text("Начать", 400, 300, arcade.color.WHITE, 24, anchor_x="center",
                                font_name="Kenney Future")
        self.btn3 = arcade.Text("Авторы", 400, 250, arcade.color.WHITE, 24, anchor_x="center",
                                font_name="Kenney Future")

    def on_draw(self):
        self.clear()
        self.title.draw()
        self.btn2.draw()
        self.btn3.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if 300 <= x <= 500:
            if 338 <= y <= 372:  # "Новая игра"
                abs = 0
            elif 288 <= y <= 322:  # "Продолжить" - ОТКРЫВАЕМ DORS_WINDOW
                self.open_dors_window()  # ← ВЫЗЫВАЕМ НОВЫЙ МЕТОД
            elif 238 <= y <= 272:  # "Авторы"
                from authors_window import AuthorsWindow
                self.window.show_view(AuthorsWindow())

    def open_dors_window(self):
        #Открывает окно выбора дверей (старую игру) из pyfile
        try:
            # Импортируем DorsWindow из pyfile
            import sys
            import os

            # Получаем путь к pyfile
            current_dir = os.path.dirname(os.path.abspath(__file__))  # v2/
            parent_dir = os.path.dirname(current_dir)  # v5/
            pyfile_path = os.path.join(parent_dir, "pyfile")

            # Добавляем pyfile в путь для импорта
            sys.path.insert(0, pyfile_path)

            # Теперь импортируем
            from dors_window import DorsView  # ← ИСПРАВЛЕНО!

            # Создаем DorsWindow View и показываем его в ТОМ ЖЕ окне
            dors_view = DorsView()
            self.window.show_view(dors_view)  # ← ВАЖНО: меняем View, а не окно!

        except ImportError as e:
            # Возвращаемся в меню (в том же окне)
            self.window.show_view(StartWindow())