# dors_window.py
import arcade
import random
import os
import time
from person1 import Person1
from person2 import Person2


class DorsView(arcade.View):
    def __init__(self, level=1, player=None):
        super().__init__()
        self.selected_person = None
        self.door_list = arcade.SpriteList()
        self.player = player
        self.player_spawned = False if player is None else True
        self.w_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.n_pressed = False
        self.ground_level = 100
        self.gravity = 0.5
        self.jump_force = 15
        self.player_velocity_y = 0
        self.current_door = None
        self.transition_timer = 0
        self.in_transition = False
        self.selected_folder = None
        self.level = level
        self.max_levels = 3
        self.game_completed = False

        self.load_door_images()

        # Если игрок передан (из предыдущей игры), сразу размещаем его
        if self.player and self.player_spawned:
            self.player.center_x = 600  # Середина экрана
            self.player.center_y = self.ground_level + self.player.height / 2

    def load_door_images(self):
        try:
            image_path = "../texture/dors/1.png"

            if not os.path.exists(image_path):
                for ext in ['.jpg', '.jpeg', '.png']:
                    alt_path = f"../texture/dors/1{ext}"
                    if os.path.exists(alt_path):
                        image_path = alt_path
                        break

            num_doors = random.randint(2, 3)

            for i in range(num_doors):
                sprite = arcade.Sprite(image_path, scale=0.5)
                sprite.center_y = 300
                sprite.texture_path = image_path
                self.door_list.append(sprite)

            self.arrange_images()

        except Exception as e:
            print(f"Ошибка загрузки дверей: {e}")

    def arrange_images(self):
        if not self.door_list:
            return

        num_images = len(self.door_list)
        if self.window:
            spacing = (self.window.width - 100) / (num_images + 1)

            for i, sprite in enumerate(self.door_list):
                sprite.center_x = 50 + spacing * (i + 1)

    def spawn_player(self):
        if self.selected_person == "Person1":
            self.player = Person1()
        elif self.selected_person == "Person2":
            self.player = Person2()

        if self.player:
            if self.window:
                self.player.center_x = self.window.width // 2
            self.player.center_y = self.ground_level + self.player.height / 2
            self.player_spawned = True

    def update_physics(self):
        if not self.player or not self.player_spawned:
            return

        self.player_velocity_y -= self.gravity
        self.player.center_y += self.player_velocity_y

        if self.player.center_y - self.player.height / 2 <= self.ground_level:
            self.player.center_y = self.ground_level + self.player.height / 2
            self.player_velocity_y = 0

        dx = 0
        if self.player:
            player_speed = self.player.movement_speed

            if self.a_pressed:
                dx = -player_speed
            if self.d_pressed:
                dx = player_speed

            self.player.center_x += dx

            if self.window:
                if self.player.left < 0:
                    self.player.left = 0
                if self.player.right > self.window.width:
                    self.player.right = self.window.width

    def check_door_collision(self):
        if not self.player or not self.door_list:
            return None

        for door in self.door_list:
            dx = abs(self.player.center_x - door.center_x)
            combined_half_width = (self.player.width / 2 + door.width / 2)
            border_distance_x = dx - combined_half_width

            if border_distance_x <= 0:
                return door

        return None

    def on_show(self):
        """Вызывается при показе View"""
        if self.window:
            self.window.set_size(1200, 750)
            self.arrange_images()

    def on_draw(self):
        self.clear(arcade.color.WHITE)

        # Рисуем таймер если идет переход
        if self.in_transition and self.window:
            remaining = max(0, 4 - self.transition_timer)
            arcade.draw_text(
                f"Переход через: {remaining:.1f}с",
                self.window.width // 2,
                self.window.height // 2,
                arcade.color.RED,
                32,
                align="center",
                anchor_x="center"
            )

        self.door_list.draw()

        if self.player and not self.in_transition:
            # Рисуем игрока через SpriteList (как в старом коде)
            temp_list = arcade.SpriteList()
            temp_list.append(self.player)
            temp_list.draw()

            if self.current_door:
                arcade.draw_circle_outline(
                    self.current_door.center_x,
                    self.current_door.center_y,
                    60,
                    arcade.color.RED,
                    3
                )

    def on_update(self, delta_time):
        if self.in_transition:
            self.transition_timer += delta_time

            if self.transition_timer >= 4:
                self.start_game()
            return

        self.update_physics()
        self.current_door = self.check_door_collision()

    def on_key_press(self, key, modifiers):
        if self.in_transition:
            return

        if key == arcade.key.KEY_1 or key == arcade.key.NUM_1:
            self.selected_person = "Person1"
            self.spawn_player()

        elif key == arcade.key.KEY_2 or key == arcade.key.NUM_2:
            self.selected_person = "Person2"
            self.spawn_player()

        elif key == arcade.key.W and self.player_spawned:
            if self.player_velocity_y == 0:
                self.player_velocity_y = self.jump_force

        elif key == arcade.key.A:
            self.a_pressed = True

        elif key == arcade.key.D:
            self.d_pressed = True

        elif key == arcade.key.F and self.current_door and self.player_spawned:
            self.start_transition()

        # Изменение размера окна
        elif key == arcade.key.N and self.window:
            if self.window.width == 1200:
                self.window.set_size(2000, 1500)
            else:
                self.window.set_size(1200, 750)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

    def start_transition(self):
        """Начинает переход через дверь"""
        self.in_transition = True
        self.transition_timer = 0

        # Меняем текстуру у текущей двери
        if self.current_door:
            new_path = "../texture/dors/2.png"
            if not os.path.exists(new_path):
                for ext in ['.jpg', '.jpeg', '.png']:
                    alt_path = f"../texture/dors/2{ext}"
                    if os.path.exists(alt_path):
                        new_path = alt_path
                        break

            if os.path.exists(new_path):
                self.current_door.texture = arcade.load_texture(new_path)

        # Выбираем случайный фон
        folders = ["ad", "les", "podzemel", "zamok"]
        self.selected_folder = random.choice(folders)
        print(f"Выбран фон: {self.selected_folder}")

    # В dors_window.py в методе start_game:
    def start_game(self):
        """Запускает главную игру с выбранным фоном"""
        print(f"Уровень {self.level}/{self.max_levels}")
        print(f"Передаем фон: {self.selected_folder}")

        from game import GameView

        game_view = GameView(
            selected_background_folder=self.selected_folder,
            level=self.level,
            max_levels=self.max_levels
        )

        # Используем setup_single_player если есть player
        if self.player:
            game_view.setup_single_player(self.player)
        else:
            game_view.setup()

        # Переключаем View вместо создания нового окна
        self.window.show_view(game_view)