import arcade
import random
import os
import time
from constants1 import *
from person1 import Person1
from person2 import Person2


class DorsWindow(arcade.View):  # ← ИЗМЕНЕНО НА View!
    def __init__(self, level=1, max_levels=3, player=None):
        super().__init__()
        # Размеры окна (берем из main.py)
        self.window_width = SCREEN_WIDTH  # ← Используем константу
        self.window_height = SCREEN_HEIGHT

        self.selected_person = None
        self.door_list = arcade.SpriteList()
        self.player = player  # Принимаем персонажа из предыдущего уровня
        self.player_spawned = False
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
        self.max_levels = max_levels
        self.game_completed = False

        # Если персонажа нет (первый уровень), ждем выбора
        if not self.player:
            self.show_selection_text = True
        else:
            self.show_selection_text = False
            self.player_spawned = True

        self.load_door_images()

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
                sprite.texture_path = image_path  # Сохраняем путь к текстуре
                self.door_list.append(sprite)

            self.arrange_images()

        except Exception as e:
            print(f"Ошибка загрузки изображений дверей: {e}")

    def arrange_images(self):
        if not self.door_list:
            return

        num_images = len(self.door_list)
        spacing = (self.window_width - 100) / (num_images + 1)

        for i, sprite in enumerate(self.door_list):
            sprite.center_x = 50 + spacing * (i + 1)

    def spawn_player(self):
        if not self.player:
            if self.selected_person == "Person1":
                self.player = Person1()
            elif self.selected_person == "Person2":
                self.player = Person2()
            else:
                return  # Персонаж не выбран

        if self.player:
            self.player.center_x = self.window_width // 2
            self.player.center_y = self.ground_level + self.player.height / 2
            self.player_spawned = True
            self.show_selection_text = False

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

            if self.player.left < 0:
                self.player.left = 0
            if self.player.right > self.window_width:
                self.player.right = self.window_width

    def check_door_collision(self):
        if not self.player or not self.door_list:
            return None

        for door in self.door_list:
            dx = abs(self.player.center_x - door.center_x)
            combined_half_width = (self.player.width / 2 + door.width / 2)
            border_distance_x = dx - combined_half_width

            if border_distance_x <= 0:
                return door  # Возвращаем конкретную дверь

        return None

    def on_show_view(self):
        """Вызывается при показе этого View"""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()

        # Фон
        arcade.draw_lrbt_rectangle_filled(0, self.window_width, 0, self.window_height, arcade.color.WHITE)

        self.door_list.draw()

        if self.player and self.player_spawned and not self.in_transition:
            # Отрисовываем через SpriteList (гарантированно работает)
            player_list = arcade.SpriteList()
            player_list.append(self.player)
            player_list.draw()

            if self.current_door:
                arcade.draw_circle_outline(
                    self.current_door.center_x,
                    self.current_door.center_y,
                    60,
                    arcade.color.RED,
                    3
                )
        # Текст выбора персонажа
        if self.show_selection_text:
            arcade.draw_text(
                "Выберите персонажа: 1 - Person1, 2 - Person2",
                self.window_width // 2,
                self.window_height - 50,
                arcade.color.BLACK,
                16,
                anchor_x="center"
            )

        # Таймер перехода
        if self.in_transition:
            arcade.draw_text(
                f"Переход через: {4 - int(self.transition_timer)}",
                self.window_width // 2,
                100,
                arcade.color.RED,
                24,
                anchor_x="center"
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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

    def start_transition(self):
        """Начинает переход через дверь"""
        self.in_transition = True
        self.transition_timer = 0

        # Меняем текстуру ТОЛЬКО у текущей двери (self.current_door)
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

        # Определяем какая папка выбрана для фона
        folders = ["ad", "les", "podzemel", "zamok"]
        self.selected_folder = random.choice(folders)
        print(f"DEBUG: Выбрана папка фона: {self.selected_folder}")

    def start_game(self):
        """Запускает игровое View (Game) с выбранным фоном"""
        print(f"DEBUG: Уровень {self.level}/{self.max_levels}")
        print(f"DEBUG: Передаем фон: {self.selected_folder}")

        # Импортируем Game (который тоже должен быть View!)
        from game import Game

        # Создаем игровое View и переключаемся на него
        game_view = Game(
            selected_background_folder=self.selected_folder,
            level=self.level,
            max_levels=self.max_levels,
            player=self.player  # Передаем персонажа
        )

        # Переключаем View в том же окне
        self.window.show_view(game_view)