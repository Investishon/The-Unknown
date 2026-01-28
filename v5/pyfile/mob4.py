import arcade


class Mob4(arcade.Sprite):
    def __init__(self):
        super().__init__("../mobs/mob4.jpg", 0.5)
        # СВОИ параметры для Mob4
        self.rotation_speed = 1    # Скорость вращения по кругу
        self.health = 150          # Здоровье
        self.initial_health = 150
        self.is_controlled = False
        self.attack_damage = 50      # Сила атаки
        self.attack_range = 25       # Радиус атаки
        self.attack_delay = 2.0      # 2 секунды до первой атаки
        self.attack_cooldown = 4.0   # 4 секунды кулдаун