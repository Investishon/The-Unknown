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
        self.title = arcade.Text("The Unknown", 400, 500, arcade.color.WHITE, 48, anchor_x="center", font_name="Kenney Future")
        self.btn1 = arcade.Text("Новая игра", 400, 350, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")
        self.btn2 = arcade.Text("Продолжить", 400, 300, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")
        self.btn3 = arcade.Text("Авторы", 400, 250, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")

    def on_draw(self):
        self.clear()
        self.title.draw()
        self.btn1.draw()
        self.btn2.draw()
        self.btn3.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if 300 <= x <= 500:
            if 338 <= y <= 372:
                from level_select import LevelSelect
                self.window.show_view(LevelSelect())
            elif 288 <= y <= 322:
                pass
            elif 238 <= y <= 272:
                from authors_window import AuthorsWindow
                self.window.show_view(AuthorsWindow())