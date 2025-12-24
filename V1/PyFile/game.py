import arcade
import math
import random
from constants import *
from person1 import Person1
from person2 import Person2
from mob1 import Mob1
from mob2 import Mob2
from mob3 import Mob3
from mob4 import Mob4
from mob5 import Mob5


class Game(arcade.Window):
    def __init__(self):
        super().__init__(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT, SCREEN_TITLE)
        self.all_entities = None
        self.controlled_entity = None
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        arcade.set_background_color(arcade.color.AMAZON)

        # Кнопки для спауна мобов
        self.mob_buttons = []
        self.button_width = 100
        self.button_height = 40
        self.button_margin = 10

    def setup(self):
        self.all_entities = arcade.SpriteList()

        # Спауним двух персонажей сразу (БЕЗ параметров!)
        person1 = Person1()  # ← ПУСТЫЕ СКОБКИ!
        person1.center_x = 200
        person1.center_y = 300

        person2 = Person2()  # ← ПУСТЫЕ СКОБКИ!
        person2.center_x = 500
        person2.center_y = 300

        self.all_entities.append(person1)
        self.all_entities.append(person2)

        # Создаем кнопки для мобов
        self.create_mob_buttons()

        self.controlled_entity = self.all_entities[0]
        self.controlled_entity.is_controlled = True

        # Отладочный вывод для проверки скорости
        print(f"Person1 создан: speed={person1.movement_speed}")
        print(f"Person2 создан: speed={person2.movement_speed}")

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
        """Спаун моба по ID (БЕЗ передачи параметров!)"""
        mob = None
        if mob_id == 1:
            mob = Mob1()  # ← ПУСТЫЕ СКОБКИ!
        elif mob_id == 2:
            mob = Mob2()  # ← ПУСТЫЕ СКОБКИ!
        elif mob_id == 3:
            mob = Mob3()  # ← ПУСТЫЕ СКОБКИ!
        elif mob_id == 4:
            mob = Mob4()  # ← ПУСТЫЕ СКОБКИ!
        elif mob_id == 5:
            mob = Mob5()  # ← ПУСТЫЕ СКОБКИ!

        if mob:
            # Спауним в случайном месте в правой части экрана
            mob.center_x = random.randrange(self.width - 300, self.width - 100)
            mob.center_y = random.randrange(100, self.height - 100)

            # Добавляем атрибуты для кругового движения
            mob.circle_center_x = mob.center_x  # центр круга
            mob.circle_center_y = mob.center_y
            mob.circle_radius = 50  # радиус круга
            mob.circle_angle = random.uniform(0, 2 * math.pi)  # начальный угол
            mob.circle_speed = mob.rotation_speed * 0.02  # скорость вращения

            self.all_entities.append(mob)
            print(f"Создан моб {mob_id}: rotation_speed={mob.rotation_speed}")

    def on_draw(self):
        self.clear()
        self.all_entities.draw()

        # Рисуем кнопки для мобов
        for button in self.mob_buttons:
            # Рисуем прямоугольник кнопки
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

            # Рамка кнопки
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
            "WASD - движение | Клик на персонажа - выбрать | F - раздвинуть экран",
            10, self.height - 20,
            arcade.color.WHITE, 12
        )

        # Подсказка про кнопки
        arcade.draw_text(
            "Кликните на кнопки выше для спауна мобов (двигаются по кругу)",
            10, self.height - 35,
            arcade.color.LIGHT_YELLOW, 12
        )

        # Отображение текущей скорости персонажа
        if self.controlled_entity and isinstance(self.controlled_entity, (Person1, Person2)):
            arcade.draw_text(
                f"Текущая скорость: {self.controlled_entity.movement_speed}",
                self.width - 200, self.height - 20,
                arcade.color.YELLOW, 12
            )

    def on_update(self, delta_time):
        # БЛОК 1: Управление персонажем через WASD
        if self.controlled_entity and self.controlled_entity.is_controlled:
            # Проверяем, что это персонаж (не моб!)
            if isinstance(self.controlled_entity, (Person1, Person2)):
                # Сбрасываем движение
                self.controlled_entity.change_x = 0
                self.controlled_entity.change_y = 0

                # Используем movement_speed ИЗ КЛАССА персонажа
                player_speed = self.controlled_entity.movement_speed

                if self.w_pressed:
                    self.controlled_entity.change_y = player_speed
                if self.s_pressed:
                    self.controlled_entity.change_y = -player_speed
                if self.a_pressed:
                    self.controlled_entity.change_x = -player_speed
                if self.d_pressed:
                    self.controlled_entity.change_x = player_speed

                # Обновляем позицию
                self.controlled_entity.center_x += self.controlled_entity.change_x
                self.controlled_entity.center_y += self.controlled_entity.change_y

                # Границы экрана
                if self.controlled_entity.left < 0:
                    self.controlled_entity.left = 0
                if self.controlled_entity.right > self.width:
                    self.controlled_entity.right = self.width
                if self.controlled_entity.bottom < 0:
                    self.controlled_entity.bottom = 0
                if self.controlled_entity.top > self.height:
                    self.controlled_entity.top = self.height

        # БЛОК 2: Движение мобов по кругу (НЕ персонажей!)
        for entity in self.all_entities:
            # Проверяем, что это моб (по наличию circle_radius)
            if hasattr(entity, 'circle_radius') and not entity.is_controlled:
                # Используем rotation_speed ИЗ КЛАССА моба
                entity.circle_angle += entity.circle_speed

                # Вычисляем новую позицию по кругу
                entity.center_x = entity.circle_center_x + math.cos(entity.circle_angle) * entity.circle_radius
                entity.center_y = entity.circle_center_y + math.sin(entity.circle_angle) * entity.circle_radius

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.F:
            # Раздвигаем экран на максимум
            self.set_size(MAX_SCREEN_WIDTH, MAX_SCREEN_HEIGHT)
            # Обновляем позиции кнопок
            self.create_mob_buttons()
        elif key == arcade.key.P:
            # Тестовая кнопка для проверки скорости
            if self.controlled_entity and isinstance(self.controlled_entity, (Person1, Person2)):
                print(
                    f"Текущий персонаж: {type(self.controlled_entity).__name__}, скорость={self.controlled_entity.movement_speed}")

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Проверяем клик по кнопкам мобов
            for button_data in self.mob_buttons:
                button_left = button_data['x']
                button_right = button_data['x'] + button_data['width']
                button_bottom = button_data['y'] - button_data['height'] / 2
                button_top = button_data['y'] + button_data['height'] / 2

                if (x >= button_left and x <= button_right and
                        y >= button_bottom and y <= button_top):
                    self.spawn_mob(button_data['id'])
                    return

            # Клик по существам для выбора управления - ТОЛЬКО ПЕРСОНАЖИ
            clicked = arcade.get_sprites_at_point((x, y), self.all_entities)
            if clicked:
                new_entity = clicked[0]
                # Управляем только персонажами (не мобами)
                if (isinstance(new_entity, (Person1, Person2)) and
                        new_entity != self.controlled_entity):
                    if self.controlled_entity:
                        self.controlled_entity.is_controlled = False
                    new_entity.is_controlled = True
                    self.controlled_entity = new_entity
                    print(f"Выбран персонаж: {type(new_entity).__name__}, скорость={new_entity.movement_speed}")