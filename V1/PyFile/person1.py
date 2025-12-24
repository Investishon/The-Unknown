import arcade

class Person1(arcade.Sprite):
    def __init__(self):
        super().__init__("../person/person1.jpg", 1.0)
        # ВСЕ параметры персонажа задаются ЗДЕСЬ
        self.movement_speed = 5    # Скорость движения (для WASD)
        self.health = 100          # Здоровье
        self.is_controlled = False