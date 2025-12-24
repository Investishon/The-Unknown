import arcade

class Mob3(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob3.jpg", 0.5)
        # СВОИ параметры для Mob3
        self.rotation_speed = 3    # Скорость вращения по кругу
        self.health = 200          # Здоровье
        self.is_controlled = False