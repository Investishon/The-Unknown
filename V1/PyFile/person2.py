import arcade

class Person2(arcade.Sprite):
    def __init__(self):
        super().__init__("../person/person2.jpg", 1.0)
        # СВОИ параметры для Person2
        self.movement_speed = 1    # Скорость движения (для WASD)
        self.health = 150          # Здоровье
        self.is_controlled = False