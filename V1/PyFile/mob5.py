import arcade

class Mob5(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob5.jpg", 0.5)
        # СВОИ параметры для Mob5
        self.rotation_speed = 2    # Скорость вращения по кругу
        self.health = 100          # Здоровье
        self.is_controlled = False