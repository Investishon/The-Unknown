import arcade


class Person2(arcade.Sprite):
    def __init__(self):
        super().__init__("../person/person2.jpg", 1.0)
        self.movement_speed = 10
        self.health = 150
        self.is_controlled = False
        self.punch_damage = 150      # Сила удара
        self.punch_radius = 40      # Радиус удара
        self.punch_reserve_time = 3.0  # 3 секунды резерва
        self.punch_cooldown = 0.3   # 0.3 секунд кулдаун