import arcade

class LevelSelect(arcade.View):
    def __init__(self):
        super().__init__()
        self.title = None
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.back = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.title = arcade.Text("ВЫБОР УРОВНЯ", 400, 520, arcade.color.WHITE, 32, anchor_x="center", font_name="Kenney Future")
        self.l1 = arcade.Text("Level 1", 400, 350, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")
        self.l2 = arcade.Text("Level 2", 400, 300, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")
        self.l3 = arcade.Text("Level 3", 400, 250, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")
        self.back = arcade.Text("Назад", 400, 150, arcade.color.WHITE, 24, anchor_x="center", font_name="Kenney Future")

    def on_draw(self):
        self.clear()
        self.title.draw()
        self.l1.draw()
        self.l2.draw()
        self.l3.draw()
        self.back.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if 325 <= x <= 475:
            if 338 <= y <= 372:
                print("Start level 1")
            elif 288 <= y <= 322:
                print("Start level 2")
            elif 238 <= y <= 272:
                print("Start level 3")
            elif 138 <= y <= 172:
                from start_window import StartWindow
                self.window.show_view(StartWindow())