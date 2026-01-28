import arcade
from start_window import StartWindow


class AuthorsWindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.title = None
        self.author1 = None
        self.author2 = None
        self.back = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.title = arcade.Text("The Unknown", 400, 500, arcade.color.WHITE, 48, anchor_x="center", font_name="Kenney Future")
        self.author1 = arcade.Text("Назар Пасков", 400, 350, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")
        self.author2 = arcade.Text("Максим Маслов", 400, 300, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")
        self.back = arcade.Text("Назад", 400, 200, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")

    def on_draw(self):
        self.clear()
        self.title.draw()
        self.author1.draw()
        self.author2.draw()
        self.back.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if 325 <= x <= 475 and 188 <= y <= 212:
            self.window.show_view(StartWindow())