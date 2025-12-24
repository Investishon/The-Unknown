import arcade

class Mob4(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob4.jpg", 0.5)
        # СВОИ параметры для Mob4
        self.rotation_speed = 1    # Скорость вращения по кругу
        self.health = 150          # Здоровье
        self.is_controlled = False