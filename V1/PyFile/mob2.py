import arcade

class Mob2(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob2.jpg", 0.5)
        # СВОИ параметры для Mob2
        self.rotation_speed = 2    # Скорость вращения по кругу
        self.health = 150          # Здоровье
        self.is_controlled = False