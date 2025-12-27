import arcade
import math
import random
import time
from constants import *
from person1 import Person1
from person2 import Person2
from mob1 import Mob1
from mob2 import Mob2
from mob3 import Mob3
from mob4 import Mob4
from mob5 import Mob5
from Glav_fon import BackgroundManager


class Game(arcade.Window):
    def __init__(self):
        super().__init__(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT, SCREEN_TITLE)
        self.all_entities = None
        self.controlled_entity = None
        self.player_list = None
        self.mob_list = None
        self.w_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.n_pressed = False
        self.background_manager = BackgroundManager()

        # Физический движок
        self.ground_level = 100  # Уровень земли
        self.gravity = 0.5
        self.jump_force = 15

        # Скорости персонажей
        self.player_velocities = {}  # {player_id: velocity_y}

        # Система ударов игрока
        self.contact_timers = {}
        self.reserve_time = 2.0

        # Система атак мобов
        self.mob_attack_timers = {}
        self.mob_attack_range = 20
        self.mob_attack_damage = 50
        self.mob_attack_delay = 3.0
        self.mob_attack_cooldown = 5.0

        # Параметры удара игрока
        self.punch_damage = 50

        # Кнопки для спауна мобов
        self.mob_buttons = []
        self.button_width = 100
        self.button_height = 40
        self.button_margin = 10

    def setup(self):
        self.all_entities = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.mob_list = arcade.SpriteList()

        # Спауним двух персонажей
        person1 = Person1()
        person1.center_x = 200
        person1.center_y = self.ground_level + person1.height / 2
        person1.is_controlled = False

        person2 = Person2()
        person2.center_x = 500
        person2.center_y = self.ground_level + person2.height / 2
        person2.is_controlled = False

        self.all_entities.append(person1)
        self.all_entities.append(person2)
        self.player_list.append(person1)
        self.player_list.append(person2)

        # Инициализируем скорости
        self.player_velocities[id(person1)] = 0
        self.player_velocities[id(person2)] = 0

        self.create_mob_buttons()
        self.controlled_entity = person1
        self.controlled_entity.is_controlled = True

        print(f"Person1 создан: speed={person1.movement_speed}, health={person1.health}")
        print(f"Person2 создан: speed={person2.movement_speed}, health={person2.health}")

    def create_mob_buttons(self):
        """Создание кнопок для спауна мобов"""
        for i in range(5):
            button_x = 10
            button_y = SCREEN_HEIGHT - 50 - i * (self.button_height + self.button_margin)
            self.mob_buttons.append({
                'id': i + 1,
                'x': button_x,
                'y': button_y,
                'width': self.button_width,
                'height': self.button_height,
                'text': f"Моб {i + 1}"
            })

    def spawn_mob(self, mob_id):
        """Спаун моба по ID"""
        mob = None
        if mob_id == 1:
            mob = Mob1()
        elif mob_id == 2:
            mob = Mob2()
        elif mob_id == 3:
            mob = Mob3()
        elif mob_id == 4:
            mob = Mob4()
        elif mob_id == 5:
            mob = Mob5()

        if mob:
            mob.center_x = random.randrange(self.width - 300, self.width - 100)
            mob.center_y = self.ground_level + mob.height / 2

            self.all_entities.append(mob)
            self.mob_list.append(mob)
            print(f"Создан моб {mob_id}: health={mob.health}")

    def check_player_collision(self, player, dx, dy):
        """Проверяет столкновения персонажа с мобами"""
        old_x = player.center_x
        old_y = player.center_y

        # Пробуем переместить
        player.center_x += dx
        player.center_y += dy

        # Проверяем столкновения
        colliding_mobs = player.collides_with_list(self.mob_list)

        if colliding_mobs:
            # Если есть столкновение, откатываем движение
            player.center_x = old_x
            player.center_y = old_y
            return False

        return True

    def update_physics(self):
        """Обновляет физику для всех объектов"""
        # Физика для персонажей
        for player in self.player_list:
            player_id = id(player)

            # Применяем гравитацию
            self.player_velocities[player_id] -= self.gravity

            # Пробуем переместить по Y
            new_y = player.center_y + self.player_velocities[player_id]

            # Проверяем землю
            if new_y - player.height / 2 <= self.ground_level:
                new_y = self.ground_level + player.height / 2
                self.player_velocities[player_id] = 0

            # Проверяем столкновения с мобами по вертикали
            old_y = player.center_y
            player.center_y = new_y

            if player.collides_with_list(self.mob_list):
                player.center_y = old_y
                self.player_velocities[player_id] = 0

    def update_contact_system(self):
        """Обновляет систему контактов игрока"""
        if not self.controlled_entity:
            return

        player = self.controlled_entity
        current_time = time.time()

        for mob in self.mob_list:
            mob_id = id(mob)

            # Расстояние между границами по X
            dx = abs(player.center_x - mob.center_x)
            combined_half_width = (player.width / 2 + mob.width / 2)
            border_distance_x = dx - combined_half_width

            # Если границы достаточно близко по X (≤ 30px)
            if border_distance_x <= 30:
                self.contact_timers[mob_id] = current_time + self.reserve_time

    def process_mob_attacks(self):
        """Обрабатывает атаки мобов"""
        current_time = time.time()
        players_to_remove = []

        for mob in self.mob_list:
            mob_id = id(mob)

            if mob_id not in self.mob_attack_timers:
                self.mob_attack_timers[mob_id] = {
                    "last_attack": 0,
                    "cooldown_end": 0,
                    "player_in_range": False,
                    "range_entered_time": 0
                }

            timer_data = self.mob_attack_timers[mob_id]

            # Проверяем всех персонажей в радиусе 20px
            player_in_range = False
            target_player = None

            for player in self.player_list:
                # Расстояние между границами
                dx = abs(mob.center_x - player.center_x)
                dy = abs(mob.center_y - player.center_y)

                combined_half_width = (mob.width / 2 + player.width / 2)
                combined_half_height = (mob.height / 2 + player.height / 2)

                border_distance_x = dx - combined_half_width
                border_distance_y = dy - combined_half_height

                # Персонаж в радиусе 20px от границы
                if border_distance_x <= 20 and border_distance_y <= 20:
                    player_in_range = True
                    target_player = player
                    break

            if player_in_range and not timer_data["player_in_range"]:
                timer_data["player_in_range"] = True
                timer_data["range_entered_time"] = current_time

            elif not player_in_range and timer_data["player_in_range"]:
                timer_data["player_in_range"] = False
                timer_data["range_entered_time"] = 0

            # Логика атаки
            if player_in_range and target_player:
                can_attack = False

                if timer_data["last_attack"] == 0:
                    time_in_range = current_time - timer_data["range_entered_time"]
                    if time_in_range >= self.mob_attack_delay:
                        can_attack = True
                else:
                    if current_time >= timer_data["cooldown_end"]:
                        can_attack = True

                if can_attack:
                    target_player.health -= self.mob_attack_damage

                    timer_data["last_attack"] = current_time
                    timer_data["cooldown_end"] = current_time + self.mob_attack_cooldown

                    print(f"Моб атаковал {type(target_player).__name__}!")
                    print(f"  Здоровье: {target_player.health}")

                    if target_player.health <= 0:
                        print(f"  {type(target_player).__name__} УБИТ!")
                        players_to_remove.append(target_player)

        # Удаляем мертвых персонажей
        for player in players_to_remove:
            self.player_list.remove(player)
            self.all_entities.remove(player)
            player_id = id(player)

            if player_id in self.player_velocities:
                del self.player_velocities[player_id]

            if player == self.controlled_entity:
                self.controlled_entity = None

                if self.player_list:
                    self.controlled_entity = self.player_list[0]
                    self.controlled_entity.is_controlled = True
                    print(f"Управление переключено на {type(self.controlled_entity).__name__}")
                else:
                    print("Все персонажи мертвы!")

    def process_punch(self):
        """Обрабатывает удар игрока"""
        if not self.controlled_entity or not self.n_pressed:
            return

        player = self.controlled_entity
        current_time = time.time()
        damaged = False

        mobs_to_remove = []

        for mob in self.mob_list:
            mob_id = id(mob)

            dx = abs(player.center_x - mob.center_x)
            combined_half_width = (player.width / 2 + mob.width / 2)
            border_distance_x = dx - combined_half_width

            borders_close = border_distance_x <= 30

            timer_active = False
            if mob_id in self.contact_timers:
                if current_time <= self.contact_timers[mob_id]:
                    timer_active = True

            if borders_close or timer_active:
                if borders_close:
                    self.contact_timers[mob_id] = current_time + self.reserve_time

                mob.health -= self.punch_damage
                damaged = True

                print(f"Удар по мобу! Здоровье: {mob.health}")

                if mob.health <= 0:
                    print(f"Моб УНИЧТОЖЕН!")
                    mobs_to_remove.append(mob)

        for mob in mobs_to_remove:
            self.mob_list.remove(mob)
            self.all_entities.remove(mob)
            mob_id = id(mob)
            if mob_id in self.contact_timers:
                del self.contact_timers[mob_id]
            if mob_id in self.mob_attack_timers:
                del self.mob_attack_timers[mob_id]

        self.n_pressed = False

    def on_draw(self):
        self.clear()
        self.background_manager.draw(self.width, self.height)
        self.all_entities.draw()

        # Рисуем кнопки для мобов
        for button in self.mob_buttons:
            left = button['x']
            right = button['x'] + button['width']
            bottom = button['y'] - button['height'] / 2
            top = button['y'] + button['height'] / 2

            points = [
                (left, bottom),
                (right, bottom),
                (right, top),
                (left, top)
            ]
            arcade.draw_polygon_filled(points, arcade.color.GRAY)
            arcade.draw_polygon_outline(points, arcade.color.BLACK, 2)

            arcade.draw_text(
                button['text'],
                button['x'] + 10,
                button['y'] - 8,
                arcade.color.WHITE,
                14
            )

        # Круг вокруг управляемого персонажа
        if self.controlled_entity and self.controlled_entity.is_controlled:
            arcade.draw_circle_outline(
                self.controlled_entity.center_x,
                self.controlled_entity.center_y,
                30,
                arcade.color.YELLOW,
                3
            )

        # Информация
        arcade.draw_text(
            "AD - движение | W - прыжок (только управляемый) | Клик на персонажа - выбрать | N - удар | F - раздвинуть экран",
            10, self.height - 20,
            arcade.color.WHITE, 12
        )

        if self.controlled_entity and isinstance(self.controlled_entity, (Person1, Person2)):
            arcade.draw_text(
                f"Скорость: {self.controlled_entity.movement_speed} | Здоровье: {self.controlled_entity.health}",
                self.width - 250, self.height - 20,
                arcade.color.YELLOW, 12
            )

    def on_update(self, delta_time):
        # 1. Обновляем физику
        self.update_physics()

        # 2. Обновляем систему контактов
        self.update_contact_system()

        # 3. Обрабатываем атаки мобов
        self.process_mob_attacks()

        # 4. Управление персонажем
        if self.controlled_entity and self.controlled_entity.is_controlled:
            if isinstance(self.controlled_entity, (Person1, Person2)):
                dx = 0
                player_speed = self.controlled_entity.movement_speed

                if self.a_pressed:
                    dx = -player_speed
                if self.d_pressed:
                    dx = player_speed

                # Проверяем столкновения по горизонтали
                old_x = self.controlled_entity.center_x
                self.controlled_entity.center_x += dx

                if self.controlled_entity.collides_with_list(self.mob_list):
                    self.controlled_entity.center_x = old_x

                # Прыжок только для управляемого персонажа
                player_id = id(self.controlled_entity)
                if self.w_pressed and self.player_velocities[player_id] == 0:
                    self.player_velocities[player_id] = self.jump_force
                    self.w_pressed = False

                # Границы экрана
                if self.controlled_entity.left < 0:
                    self.controlled_entity.left = 0
                if self.controlled_entity.right > self.width:
                    self.controlled_entity.right = self.width

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True
        elif key == arcade.key.N:
            self.n_pressed = True
            self.process_punch()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.F:
            self.set_size(MAX_SCREEN_WIDTH, MAX_SCREEN_HEIGHT)
            self.create_mob_buttons()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False
        elif key == arcade.key.N:
            self.n_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for button_data in self.mob_buttons:
                button_left = button_data['x']
                button_right = button_data['x'] + button_data['width']
                button_bottom = button_data['y'] - button_data['height'] / 2
                button_top = button_data['y'] + button_data['height'] / 2

                if (x >= button_left and x <= button_right and
                        y >= button_bottom and y <= button_top):
                    self.spawn_mob(button_data['id'])
                    return

            clicked = arcade.get_sprites_at_point((x, y), self.all_entities)
            if clicked:
                new_entity = clicked[0]
                if (isinstance(new_entity, (Person1, Person2)) and
                        new_entity != self.controlled_entity):
                    if self.controlled_entity:
                        self.controlled_entity.is_controlled = False
                    new_entity.is_controlled = True
                    self.controlled_entity = new_entity
                    print(f"Выбран персонаж: {type(new_entity).__name__}, здоровье={new_entity.health}")