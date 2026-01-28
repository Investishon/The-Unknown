import arcade


class Barrel(arcade.Sprite):
    def __init__(self):
        super().__init__("../texture/pred/1.jpg", 0.22)
        self.is_controlled = False
        self.health = 50  # Здоровье бочки
        self.initial_health = 50