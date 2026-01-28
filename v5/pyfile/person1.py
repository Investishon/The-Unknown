import arcade


class Person1(arcade.Sprite):
    def __init__(self):
        super().__init__("../person/person1.jpg", 1.0)
        self.movement_speed = 5
        self.health = 100
        self.is_controlled = False
        self.punch_damage = 50      # Сила удара
        self.punch_radius = 30      # Радиус удара
        self.punch_reserve_time = 2.0  # 2 секунды резерва
        self.punch_cooldown = 0.5   # 0.5 секунд кулдаун между ударами