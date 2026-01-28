import arcade


class Mob1(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob1.jpg", 0.5)
        self.rotation_speed = 1
        self.health = 100
        self.initial_health = 100
        self.is_controlled = False
        self.attack_damage = 30      # Сила атаки
        self.attack_range = 20       # Радиус атаки
        self.attack_delay = 3.0      # 3 секунды до первой атаки
        self.attack_cooldown = 5.0   # 5 секунд кулдаун