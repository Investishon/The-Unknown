import arcade


class Mob3(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob3.jpg", 0.5)
        # СВОИ параметры для Mob3
        self.rotation_speed = 3    # Скорость вращения по кругу
        self.health = 200          # Здоровье
        self.initial_health = 200
        self.is_controlled = False
        self.attack_damage = 50      # Сила атаки
        self.attack_range = 25       # Радиус атаки
        self.attack_delay = 2.0      # 2 секунды до первой атаки
        self.attack_cooldown = 4.0
        # 4 секунды кулдаун