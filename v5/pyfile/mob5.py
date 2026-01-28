import arcade


class Mob5(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob5.jpg", 0.5)
        # СВОИ параметры для Mob5
        self.rotation_speed = 2    # Скорость вращения по кругу
        self.health = 100          # Здоровье
        self.initial_health = 100
        self.is_controlled = False
        self.attack_damage = 50      # Сила атаки
        self.attack_range = 25       # Радиус атаки
        self.attack_delay = 2.0      # 2 секунды до первой атаки
        self.attack_cooldown = 4.0   # 4 секунды кулдаун