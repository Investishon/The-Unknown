import arcade
import math
import os
import random
import time
from constants1 import *
from person1 import Person1
from person2 import Person2
from mob1 import Mob1
from mob2 import Mob2
from mob3 import Mob3
from mob4 import Mob4
from mob5 import Mob5
from glav_fon import BackgroundManager


class Game(arcade.Window):
    def __init__(self, selected_background_folder=None,  level=1, max_levels=3):
        super().__init__(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT, SCREEN_TITLE)

        # Сохраняем переданный фон
        self.selected_background_folder = selected_background_folder
        print(f"DEBUG_Game_init: Фон получен в конструкторе: {self.selected_background_folder}")
        self.level = level
        self.max_levels = max_levels
        self.game_paused = False
        self.pause_overlay_alpha = 180  # Прозрачность затемнения

        # Просто флаг и время
        self.score = 0
        self.mob_killed_time = None
        self.return_timer = 0
        self.mob_killed = False
        self.kill_time = None

        self.all_entities = None
        self.controlled_entity = None
        self.player_list = None
        self.mob_list = None
        self.w_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.n_pressed = False

        # Теперь создаем BackgroundManager БЕЗ авто-загрузки
        self.background_manager = BackgroundManager()

        # Физический движок
        self.ground_level = 100
        self.gravity = 0.5
        self.jump_force = 15
        self.player_velocities = {}

        # Системы таймеров
        self.contact_timers = {}
        self.mob_attack_timers = {}

    def setup(self):
        self.all_entities = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.mob_list = arcade.SpriteList()

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

        self.player_velocities[id(person1)] = 0
        self.player_velocities[id(person2)] = 0

        self.controlled_entity = person1
        self.controlled_entity.is_controlled = True

        print(
            f"Person1: punch={person1.punch_damage}, radius={person1.punch_radius}, reserve={person1.punch_reserve_time}s")
        print(
            f"Person2: punch={person2.punch_damage}, radius={person2.punch_radius}, reserve={person2.punch_reserve_time}s")

    def setup_single_player(self, player):
        print(f"DEBUG_Game: setup_single_player вызван")
        print(f"DEBUG_Game: selected_background_folder = {self.selected_background_folder}")

        self.all_entities = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.mob_list = arcade.SpriteList()

        # ПЕРСОНАЖ СПАВНИТСЯ СЛЕВА
        player.center_x = 200
        player.center_y = self.ground_level + player.height / 2
        player.is_controlled = True

        self.all_entities.append(player)
        self.player_list.append(player)
        self.player_velocities[id(player)] = 0
        self.controlled_entity = player

        # Загружаем фон из выбранной папки если есть
        if self.selected_background_folder:
            print(f"DEBUG_Game: Загружаем фон из {self.selected_background_folder}")
            self.load_specific_background(self.selected_background_folder)

            # Спаун моба в зависимости от фона
            print(f"DEBUG_Game: Спауним моба для {self.selected_background_folder}")
            self.spawn_mob_by_background()
        else:
            print(f"DEBUG_Game: selected_background_folder не установлен!")


    def spawn_mob_by_background(self):
        """Спаунит моба в зависимости от выбранного фона"""
        print(f"DEBUG: spawn_mob_by_background вызван")

        if not self.selected_background_folder:
            print(f"DEBUG: Нет папки фона для спауна моба")
            return

        # Приводим к нижнему регистру для надежности
        folder = self.selected_background_folder.lower()
        print(f"DEBUG: Папка фона: {folder}")

        mob = None

        # Моб спавнится СПРАВА от персонажа
        mob_x = self.width - 200
        mob_y = self.ground_level + 50

        # Выбираем моба по папке фона
        if folder == "ad":
            mob = Mob5()
            print(f"DEBUG: Выбран Mob5 для фона 'ad'")
        elif folder == "les":
            mob = Mob4()
            print(f"DEBUG: Выбран Mob4 для фона 'les'")
        elif folder == "podzemel":
            mob = Mob2()
            print(f"DEBUG: Выбран Mob2 для фона 'podzemel'")
        elif folder == "zamok":
            mob = Mob1()
            print(f"DEBUG: Выбран Mob1 для фона 'zamok'")

        # 20% шанс на mob3 в любой папке
        if random.random() < 0.2:
            mob = Mob3()
            print(f"DEBUG: Рандомно выбран Mob3")

        if mob:
            mob.center_x = mob_x
            mob.center_y = mob_y + mob.height / 2
            self.mob_list.append(mob)
            self.all_entities.append(mob)
            print(f"DEBUG: Спаунен {type(mob).__name__} для фона {self.selected_background_folder}")
            print(f"DEBUG: Позиция: ({mob.center_x}, {mob.center_y})")
            print(f"DEBUG: mob_list содержит {len(self.mob_list)} мобов")
        else:
            print(f"DEBUG: Не удалось создать моба!")

    def update_physics(self):
        for player in self.player_list:
            player_id = id(player)
            self.player_velocities[player_id] -= self.gravity

            new_y = player.center_y + self.player_velocities[player_id]

            if new_y - player.height / 2 <= self.ground_level:
                new_y = self.ground_level + player.height / 2
                self.player_velocities[player_id] = 0

            old_y = player.center_y
            player.center_y = new_y

            if player.collides_with_list(self.mob_list):
                player.center_y = old_y
                self.player_velocities[player_id] = 0

    def update_contact_system(self):
        if not self.controlled_entity:
            return

        player = self.controlled_entity
        current_time = time.time()

        for mob in self.mob_list:
            mob_id = id(mob)

            dx = abs(player.center_x - mob.center_x)
            combined_half_width = (player.width / 2 + mob.width / 2)
            border_distance_x = dx - combined_half_width

            if border_distance_x <= player.punch_radius:
                self.contact_timers[mob_id] = current_time + player.punch_reserve_time

    def process_mob_attacks(self):
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

            player_in_range = False
            target_player = None

            for player in self.player_list:
                dx = abs(mob.center_x - player.center_x)
                dy = abs(mob.center_y - player.center_y)

                combined_half_width = (mob.width / 2 + player.width / 2)
                combined_half_height = (mob.height / 2 + player.height / 2)

                border_distance_x = dx - combined_half_width
                border_distance_y = dy - combined_half_height

                if border_distance_x <= mob.attack_range and border_distance_y <= mob.attack_range:
                    player_in_range = True
                    target_player = player
                    break

            if player_in_range and not timer_data["player_in_range"]:
                timer_data["player_in_range"] = True
                timer_data["range_entered_time"] = current_time

            elif not player_in_range and timer_data["player_in_range"]:
                timer_data["player_in_range"] = False
                timer_data["range_entered_time"] = 0

            if player_in_range and target_player:
                can_attack = False

                if timer_data["last_attack"] == 0:
                    time_in_range = current_time - timer_data["range_entered_time"]
                    if time_in_range >= mob.attack_delay:
                        can_attack = True
                else:
                    if current_time >= timer_data["cooldown_end"]:
                        can_attack = True

                if can_attack:
                    target_player.health -= mob.attack_damage

                    timer_data["last_attack"] = current_time
                    timer_data["cooldown_end"] = current_time + mob.attack_cooldown

                    print(f"Моб атаковал {type(target_player).__name__}!")
                    print(f"  Нанесено {mob.attack_damage} урона")
                    print(f"  Здоровье: {target_player.health}")

                    if target_player.health <= 0:
                        print(f"  {type(target_player).__name__} УБИТ!")
                        players_to_remove.append(target_player)

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
        if not self.controlled_entity or not self.n_pressed:
            return

        player = self.controlled_entity
        current_time = time.time()

        mobs_to_remove = []

        for mob in self.mob_list:
            mob_id = id(mob)

            dx = abs(player.center_x - mob.center_x)
            combined_half_width = (player.width / 2 + mob.width / 2)
            border_distance_x = dx - combined_half_width

            borders_close = border_distance_x <= player.punch_radius

            timer_active = False
            if mob_id in self.contact_timers:
                if current_time <= self.contact_timers[mob_id]:
                    timer_active = True

            if borders_close or timer_active:
                if borders_close:
                    self.contact_timers[mob_id] = current_time + player.punch_reserve_time

                mob.health -= player.punch_damage

                if mob.health <= 0:
                    mobs_to_remove.append(mob)

                    # ДОБАВЛЯЕМ ОЧКИ ЗА УБИЙСТВО МОБА
                    # Очки = исходное здоровье моба (health до урона)
                    if hasattr(mob, 'initial_health'):
                        self.score += mob.initial_health
                    else:
                        # Если initial_health нет, используем текущее health
                        # Но лучше добавить initial_health при создании моба
                        self.score += 100  # базовые очки

                    print(f"Моб убит! Очки: {self.score}")
                    self.mob_killed = True
                    self.kill_time = current_time

        for mob in mobs_to_remove:
            self.mob_list.remove(mob)
            self.all_entities.remove(mob)
            mob_id = id(mob)
            if mob_id in self.contact_timers:
                del self.contact_timers[mob_id]
            if mob_id in self.mob_attack_timers:
                del self.mob_attack_timers[mob_id]

        self.n_pressed = False

    def draw_health_bars(self):
        """Рисует цифры здоровья над мобами"""
        for mob in self.mob_list:
            text_x = mob.center_x
            text_y = mob.center_y + mob.height / 2 + 15

            arcade.draw_text(
                str(mob.health),
                text_x, text_y,
                arcade.color.GREEN, 14,
                align="center", anchor_x="center", anchor_y="center"
            )

    def load_specific_background(self, folder_name):
        """Загружает фон из конкретной папки"""
        try:
            folder_path = f"../texture/{folder_name}"
            if not os.path.exists(folder_path):
                return

            files = [f for f in os.listdir(folder_path)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if files:
                random_file = random.choice(files)
                file_path = os.path.join(folder_path, random_file)
                self.background_manager.background_texture = arcade.load_texture(file_path)
                print(f"Загружен фон: {folder_name}/{random_file}")

        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")

    def on_draw(self):
        self.clear()
        self.background_manager.draw(self.width, self.height)
        self.all_entities.draw()

        # Рисуем здоровье мобов
        self.draw_health_bars()

        # Круг вокруг управляемого персонажа
        if self.controlled_entity and self.controlled_entity.is_controlled:
            arcade.draw_circle_outline(
                self.controlled_entity.center_x,
                self.controlled_entity.center_y,
                30,
                arcade.color.YELLOW,
                3
            )

        # Управление
        arcade.draw_text(
            "AD-движение W-прыжок N-удар ESC-пауза",
            10, self.height - 60,
            arcade.color.WHITE, 12
        )

        # Если моб убит
        if self.mob_killed:
            arcade.draw_text(
                "Моб убит! Возврат через несколько секунд...",
                self.width // 2, 50,
                arcade.color.GREEN, 18,
                align="center", anchor_x="center"
            )

        # Если игра на паузе - рисуем затемнение и надпись
        if self.game_paused:
            # Рисуем два больших треугольника чтобы покрыть весь экран
            # Верхний треугольник
            arcade.draw_triangle_filled(
                0, self.height,  # левый верх
                self.width, self.height,  # правый верх
                self.width // 2, 0,  # середина низа
                arcade.color.BLACK
            )

            # Нижний треугольник
            arcade.draw_triangle_filled(
                0, 0,  # левый низ
                self.width, 0,  # правый низ
                self.width // 2, self.height,  # середина верха
                arcade.color.BLACK
            )

            #  надпись ПАУЗА
            arcade.draw_text(
                "ПАУЗА",
                self.width // 2,
                self.height // 2 + 50,
                arcade.color.YELLOW,
                64,
                align="center",
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            # Подсказка
            arcade.draw_text(
                "Нажмите ESC для продолжения",
                self.width // 2,
                self.height // 2 - 50,
                arcade.color.WHITE,
                24,
                align="center",
                anchor_x="center",
                anchor_y="center"
            )

            # Информация о состоянии игры
            if self.controlled_entity:
                arcade.draw_text(
                    f"Уровень: {self.level}",
                    self.width // 2,
                    self.height // 2 - 100,
                    arcade.color.LIGHT_BLUE,
                    20,
                    align="center",
                    anchor_x="center",
                    anchor_y="center"
                )
        # В методе on_draw добавьте отображение текущих очков:
        if self.controlled_entity and isinstance(self.controlled_entity, (Person1, Person2)):
            arcade.draw_text(
                f"Здоровье: {self.controlled_entity.health} | Скорость: {self.controlled_entity.movement_speed}",
                self.width - 400, self.height - 30,  # ← измените позицию если нужно
                arcade.color.YELLOW, 16
            )


    def on_update(self, delta_time):

        # Если моб убит и прошло 10 секунд
        if self.mob_killed and self.kill_time:
            if time.time() - self.kill_time >= 10:
                self.go_back_to_dors()
                return
        # Если игра на паузе - не обновляем логику
        if self.game_paused:
            return

        # Проверяем убийство моба и время
        if self.mob_killed and self.kill_time:
            if time.time() - self.kill_time >= 10:
                self.go_back_to_dors()
                return

        # Обычная логика игры
        self.update_physics()
        self.update_contact_system()
        self.process_mob_attacks()

        if self.controlled_entity and self.controlled_entity.is_controlled:
            if isinstance(self.controlled_entity, (Person1, Person2)):
                dx = 0
                player_speed = self.controlled_entity.movement_speed

                if self.a_pressed:
                    dx = -player_speed
                if self.d_pressed:
                    dx = player_speed

                old_x = self.controlled_entity.center_x
                self.controlled_entity.center_x += dx

                if self.controlled_entity.collides_with_list(self.mob_list):
                    self.controlled_entity.center_x = old_x

                player_id = id(self.controlled_entity)
                if self.w_pressed and self.player_velocities[player_id] == 0:
                    self.player_velocities[player_id] = self.jump_force
                    self.w_pressed = False

                if self.controlled_entity.left < 0:
                    self.controlled_entity.left = 0
                if self.controlled_entity.right > self.width:
                    self.controlled_entity.right = self.width

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # Переключаем паузу по ESC
            self.game_paused = not self.game_paused
            print(f"Игра {'приостановлена' if self.game_paused else 'возобновлена'}")
            return  # Важно: return чтобы не обрабатывались другие действия

        # Если игра на паузе - блокируем остальные клавиши
        if self.game_paused:
            return

        # Обычная обработка клавиш
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True
        elif key == arcade.key.F:
            self.n_pressed = True
            self.process_punch()
        elif key == arcade.key.N:
            self.set_size(MAX_SCREEN_WIDTH, MAX_SCREEN_HEIGHT)

    def on_key_release(self, key, modifiers):
        # Если игра на паузе - блокируем
        if self.game_paused:
            return

        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False
        elif key == arcade.key.N:
            self.n_pressed = False

    def go_back_to_dors(self):
        """Возвращаемся в DorsWindow или показываем финальное окно"""
        print(f"Уровень {self.level} завершен!")
        print(f"Очки: {self.score}")  # Добавим для отладки

        # Если игрок умер - поражение
        if not self.controlled_entity or (self.controlled_entity and self.controlled_entity.health <= 0):
            print("Игрок умер - показываем поражение")
            self.show_final_window("defeat")
            return

        # Если все уровни пройдены - победа
        if self.level >= self.max_levels:
            print("Все уровни пройдены - показываем победу")
            self.show_final_window("victory")  # ← ЗДЕСЬ ИЗМЕНЕНИЕ!
            return

        # Иначе продолжаем игру
        arcade.close_window()
        time.sleep(0.1)

        from dors_window import DorsWindow
        dors = DorsWindow()
        dors.level = self.level + 1  # Увеличиваем уровень

        # Сохраняем персонажа если есть
        if hasattr(self, 'controlled_entity'):
            dors.player = self.controlled_entity

        arcade.run()

    def show_final_window(self, result):
        """Показывает финальное окно с результатами"""
        print(f"=== ПОКАЗЫВАЕМ ФИНАЛЬНОЕ ОКНО ===")
        print(f"Результат: {result}")
        print(f"Очки: {self.score}")
        print(f"Уровень: {self.level}")

        # Закрываем текущее окно игры
        arcade.close_window()
        time.sleep(0.5)

        try:
            # Импортируем финальное окно
            from final_window import FinalWindow

            # Определяем сколько уровней пройдено
            if result == "victory":
                levels_completed = self.level  # 3 уровня пройдено
            else:  # поражение
                levels_completed = max(0, self.level - 1)  # на 1 меньше

            print(f"Уровней пройдено: {levels_completed}")

            # Создаем новое окно для финального экрана
            window = arcade.Window(800, 600, "The Unknown")

            # Создаем финальное представление
            final_view = FinalWindow(
                result=result,
                score=self.score,
                levels_completed=levels_completed,
                total_levels=self.max_levels
            )

            # Показываем финальное окно
            window.show_view(final_view)

            # Запускаем новый цикл отрисовки
            arcade.run()

        except ImportError as e:
            print(f"Ошибка импорта FinalWindow: {e}")
            print("Просто закрываю игру...")
        except Exception as e:
            print(f"Другая ошибка: {e}")
            import traceback
            traceback.print_exc()

