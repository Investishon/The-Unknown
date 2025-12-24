import arcade

class Mob1(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob1.jpg", 0.5)
        # ВСЕ параметры моба задаются ЗДЕСЬ
        self.rotation_speed = 1    # Скорость вращения по кругу
        self.health = 100          # Здоровье
        self.is_controlled = False