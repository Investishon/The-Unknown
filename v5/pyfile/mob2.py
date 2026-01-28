import arcade


class Mob2(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob2.jpg", 0.5)
        self.rotation_speed = 2
        self.health = 150
        self.initial_health = 150
        self.is_controlled = False
        self.attack_damage = 50      # Сила атаки
        self.attack_range = 25       # Радиус атаки
        self.attack_delay = 2.0      # 2 секунды до первой атаки
        self.attack_cooldown = 4.0   # 4 секунды кулдаун