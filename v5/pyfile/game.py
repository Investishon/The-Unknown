import arcade
import os
import random
import time
from person1 import Person1
from person2 import Person2
from mob1 import Mob1
from mob2 import Mob2
from mob3 import Mob3
from mob4 import Mob4
from mob5 import Mob5
from glav_fon import BackgroundManager
from barrel import Barrel

# Глобальная переменная для музыки
background_music = None

class DustParticle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(1.5, 3.5)  # Маленькие частицы
        # ТЕМНО-СЕРЫЕ цвета
        self.color = (
            random.randint(80, 100),  # Темно-серый R
            random.randint(80, 100),  # Темно-серый G
            random.randint(80, 100),  # Темно-серый B
            random.randint(120, 160)  # Средняя прозрачность
        )
        self.speed_x = random.uniform(-0.2, 0.2)  # Легкое движение по X
        self.speed_y = random.uniform(-1.5, -0.8)  # Падение вниз
        self.lifetime = random.uniform(2, 4)  # Время жизни
        self.alpha = self.color[3]  # Начальная прозрачность
        self.created_time = time.time()

    def update(self):
        current_time = time.time()
        elapsed = current_time - self.created_time

        # Движение
        self.x += self.speed_x
        self.y += self.speed_y

        # Затухание
        life_progress = elapsed / self.lifetime
        self.alpha = int(self.color[3] * (1 - life_progress))

        # Возвращаем True если частица еще жива
        return elapsed < self.lifetime and self.alpha > 10

    def draw(self):
        # Рисуем простой круг
        if self.alpha > 10:
            arcade.draw_circle_filled(
                self.x, self.y, self.size,
                (self.color[0], self.color[1], self.color[2], self.alpha)
            )


class GameView(arcade.View):
    def __init__(self, selected_background_folder=None, level=1, max_levels=3):
        super().__init__()
        self.selected_background_folder = selected_background_folder
        self.level = level
        self.max_levels = max_levels
        self.game_paused = False
        self.pause_overlay_alpha = 180

        # Загружаем очки из файла при создании
        self.total_score = self.load_score_from_file()
        self.level_score = 0  # Очки за текущий уровень
        self.score = self.total_score + self.level_score  # Общие очки

        self.mob_killed_time = None
        self.return_timer = 0
        self.mob_killed = False
        self.kill_time = None

        self.all_entities = None
        self.controlled_entity = None
        self.player_list = None
        self.mob_list = None
        self.barrel_list = None
        self.w_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.n_pressed = False
        self.f_pressed = False

        self.background_manager = BackgroundManager()

        self.ground_level = 100  # Уровень земли
        self.gravity = 0.5
        self.jump_force = 15
        self.player_velocities = {}

        self.contact_timers = {}
        self.mob_attack_timers = {}

        # Система частиц пыли
        self.dust_particles = []
        self.particle_timer = 0
        self.particles_per_second = 25
        self.max_particles = 200

    def load_score_from_file(self):
        try:
            if os.path.exists("coin.txt"):
                with open("coin.txt", "r") as f:
                    content = f.read().strip()
                    if content:
                        return int(content)
            return 0
        except Exception as e:
            return 0

    def save_score_to_file(self, score):
        try:
            with open("coin.txt", "w") as f:
                f.write(str(score))
        except Exception as e:
            pass

    def clear_score_file(self):
        try:
            with open("coin.txt", "w") as f:
                f.write("0")
        except Exception as e:
            pass

    def update_score_display(self):
        #Обновляет отображаемые очки (сумма общих и уровня)
        self.score = self.total_score + self.level_score

    def play_background_music(self):
        #Включает случайную фоновую музыку из 4 песен
        global background_music, music_player

        # Останавливаем текущую музыку
        self.stop_background_music()

        # 4 песни в папке sound
        music_files = [
            "../sound/1.mp3",
            "../sound/2.mp3",
            "../sound/3.mp3",
            "../sound/4.mp3",
            "../sound/1.wav",
            "../sound/2.wav",
            "../sound/3.wav",
            "../sound/4.wav",
            "../sound/1.ogg",
            "../sound/2.ogg",
            "../sound/3.ogg",
            "../sound/4.ogg"
        ]

        available_music = []
        for music_file in music_files:
            if os.path.exists(music_file):
                available_music.append(music_file)

        if available_music:
            # Выбираем случайный трек
            chosen_music = random.choice(available_music)
            try:
                background_music = arcade.Sound(chosen_music, streaming=True)
                music_player = background_music.play(volume=0.3)  # Громкость 30%
            except Exception as e:
                background_music = None
                music_player = None

    def stop_background_music(self):
        #Останавливает фоновую музыку"""
        global background_music, music_player
        if background_music and music_player:
            background_music.stop(music_player)
            background_music = None
            music_player = None

    def setup(self):
        self.all_entities = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.mob_list = arcade.SpriteList()
        self.barrel_list = arcade.SpriteList()

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

        self.spawn_barrel()

    def setup_single_player(self, player):
        # ВКЛЮЧАЕМ МУЗЫКУ ПРИ ЗАПУСКЕ УРОВНЯ
        self.play_background_music()

        self.all_entities = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.mob_list = arcade.SpriteList()
        self.barrel_list = arcade.SpriteList()

        player.center_x = 200
        player.center_y = self.ground_level + player.height / 2
        player.is_controlled = True

        self.all_entities.append(player)
        self.player_list.append(player)
        self.player_velocities[id(player)] = 0
        self.controlled_entity = player

        self.spawn_barrel()

        if self.selected_background_folder:
            self.load_specific_background(self.selected_background_folder)
            self.spawn_mob_by_background()

    def update_dust_particles(self, delta_time):
        #Обновляет систему частиц пыли - ТОЛЬКО ПАДАЮЩИЕ
        if not self.window:
            return

        self.particle_timer += delta_time

        # Спауним новые частицы
        particles_to_spawn = int(self.particle_timer * self.particles_per_second)
        if particles_to_spawn > 0 and len(self.dust_particles) < self.max_particles:
            self.particle_timer = 0

            for _ in range(min(particles_to_spawn, 5)):
                spawn_x = random.uniform(0, self.window.width)
                spawn_y = self.window.height + 50  # Сверху экрана

                particle = DustParticle(spawn_x, spawn_y)
                self.dust_particles.append(particle)

        # Обновляем существующие частицы
        alive_particles = []
        for particle in self.dust_particles:
            if particle.update():
                if particle.y > -50:  # Если не ушла слишком низко
                    alive_particles.append(particle)
        self.dust_particles = alive_particles

    def spawn_barrel(self):
        #Создает бочку, проверяя чтобы не пересекалась с игроком
        try:
            max_attempts = 10
            for attempt in range(max_attempts):
                barrel = Barrel()

                if self.window:
                    min_x = 300  # Отступ от краев
                    max_x = self.window.width - 300
                    barrel.center_x = random.randint(min_x, max_x)
                else:
                    barrel.center_x = 600

                barrel.center_y = self.ground_level + barrel.height / 2

                # Проверяем коллизию только с игроком (персонажем)
                collision_with_player = False
                for player in self.player_list:
                    dx = abs(barrel.center_x - player.center_x)
                    dy = abs(barrel.center_y - player.center_y)
                    combined_half_width = (barrel.width / 2 + player.width / 2)
                    combined_half_height = (barrel.height / 2 + player.height / 2)

                    # Если пересекаются по X и Y
                    if dx < combined_half_width and dy < combined_half_height:
                        collision_with_player = True
                        break

                # Если нет коллизии с игроком, добавляем бочку
                if not collision_with_player:
                    self.barrel_list.append(barrel)
                    self.all_entities.append(barrel)
                    return

        except Exception as e:
            pass

    def check_barrel_collision(self):
        #Проверяет, находится ли игрок рядом с бочкой для разрушения
        if not self.controlled_entity or not self.barrel_list:
            return None

        player = self.controlled_entity

        for barrel in self.barrel_list:
            dx = abs(player.center_x - barrel.center_x)
            combined_half_width = (player.width / 2 + barrel.width / 2)
            border_distance_x = dx - combined_half_width

            if border_distance_x <= 30:
                return barrel

        return None

    def process_barrel_destruction(self):
        #Разрушает бочку, если игрок нажал F и рядом с ней
        if not self.f_pressed:
            return

        barrel = self.check_barrel_collision()
        if barrel:
            barrel_damage = 50
            barrel.health -= barrel_damage

            if barrel.health <= 0:
                self.barrel_list.remove(barrel)
                self.all_entities.remove(barrel)
                self.level_score += 25
                self.update_score_display()
        self.f_pressed = False

    def spawn_mob_by_background(self):

        if not self.selected_background_folder:
            return
        folder = self.selected_background_folder.lower()
        mob = None
        mob_x = self.window.width - 200 if self.window else 1000
        # Моб на уровне земли (ground_level = 100)
        mob_y = self.ground_level

        if folder == "ad":
            mob = Mob5()
        elif folder == "les":
            mob = Mob4()
        elif folder == "podzemel":
            mob = Mob2()
        elif folder == "zamok":
            mob = Mob1()
        if random.random() < 0.2:
            mob = Mob3()
        if mob:
            mob.center_x = mob_x
            mob.center_y = mob_y + mob.height / 2  # Центрируем на уровне земли
            self.mob_list.append(mob)
            self.all_entities.append(mob)

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

            if player.collides_with_list(self.mob_list) or player.collides_with_list(self.barrel_list):
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

                    if hasattr(mob, 'initial_health'):
                        self.level_score += mob.initial_health
                    else:
                        self.level_score += 100

                    self.update_score_display()
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
        for mob in self.mob_list:
            text_x = mob.center_x
            text_y = mob.center_y + mob.height / 2 + 15

            arcade.draw_text(
                str(mob.health),
                text_x, text_y,
                arcade.color.GREEN, 14,
                align="center", anchor_x="center", anchor_y="center"
            )

        for barrel in self.barrel_list:
            text_x = barrel.center_x
            text_y = barrel.center_y + barrel.height / 2 + 15

            arcade.draw_text(
                str(barrel.health),
                text_x, text_y,
                arcade.color.BROWN, 14,
                align="center", anchor_x="center", anchor_y="center"
            )

    def load_specific_background(self, folder_name):
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
            pass


    def on_draw(self):
        self.clear()

        # Рисуем фон
        self.background_manager.draw(self.window.width, self.window.height) if self.window else None

        # Рисуем частицы пыли (под всеми объектами)
        for particle in self.dust_particles:
            particle.draw()

        # Рисуем все игровые объекты
        self.all_entities.draw()

        self.draw_health_bars()

        if self.controlled_entity and self.controlled_entity.is_controlled:
            arcade.draw_circle_outline(
                self.controlled_entity.center_x,
                self.controlled_entity.center_y,
                30,
                arcade.color.YELLOW,
                3
            )

            # Показываем подсказку для разрушения бочки
            barrel = self.check_barrel_collision()
            if barrel and self.window:
                arcade.draw_text(
                    "Нажмите F чтобы разрушить бочку",
                    self.window.width // 2,
                    80,
                    arcade.color.YELLOW, 16,
                    align="center", anchor_x="center"
                )

        if self.window:
            arcade.draw_text(
                "AD-движение W-прыжок N-удар F-разрушить бочку ESC-пауза",
                10, self.window.height - 60,
                arcade.color.WHITE, 12
            )

        if self.mob_killed and self.window:
            arcade.draw_text(
                "Моб убит! Возврат через несколько секунд...",
                self.window.width // 2, 50,
                arcade.color.GREEN, 18,
                align="center", anchor_x="center"
            )

        if self.game_paused and self.window:
            arcade.draw_triangle_filled(
                0, self.window.height,
                self.window.width, self.window.height,
                self.window.width // 2, 0,
                arcade.color.BLACK
            )

            arcade.draw_triangle_filled(
                0, 0,
                self.window.width, 0,
                self.window.width // 2, self.window.height,
                arcade.color.BLACK
            )

            arcade.draw_text(
                "ПАУЗА",
                self.window.width // 2,
                self.window.height // 2 + 50,
                arcade.color.YELLOW,
                64,
                align="center",
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            arcade.draw_text(
                "Нажмите ESC для продолжения",
                self.window.width // 2,
                self.window.height // 2 - 50,
                arcade.color.WHITE,
                24,
                align="center",
                anchor_x="center",
                anchor_y="center"
            )

        if self.window and self.controlled_entity and isinstance(self.controlled_entity, (Person1, Person2)):
            arcade.draw_text(
                f"Здоровье: {self.controlled_entity.health} | Скорость: {self.controlled_entity.movement_speed} | Очки: {self.score} (Уровень: {self.level_score})",
                self.window.width - 400, self.window.height - 30,
                arcade.color.YELLOW, 16
            )

    def on_update(self, delta_time):
        if self.mob_killed and self.kill_time:
            if time.time() - self.kill_time >= 10:
                self.go_back_to_dors()
                return

        if self.game_paused:
            return

        # Обновляем частицы ВСЕГДА
        self.update_dust_particles(delta_time)

        if not self.game_paused:
            self.update_physics()
            self.update_contact_system()
            self.process_mob_attacks()
            self.process_barrel_destruction()

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

                    if self.controlled_entity.collides_with_list(
                            self.mob_list) or self.controlled_entity.collides_with_list(self.barrel_list):
                        self.controlled_entity.center_x = old_x

                    player_id = id(self.controlled_entity)
                    if self.w_pressed and self.player_velocities[player_id] == 0:
                        self.player_velocities[player_id] = self.jump_force
                        self.w_pressed = False

                    if self.window:
                        if self.controlled_entity.left < 0:
                            self.controlled_entity.left = 0
                        if self.controlled_entity.right > self.window.width:
                            self.controlled_entity.right = self.window.width

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.game_paused = not self.game_paused
            return

        if self.game_paused:
            return

        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True
        elif key == arcade.key.N:
            self.n_pressed = True
            self.process_punch()
        elif key == arcade.key.F:
            self.f_pressed = True
            self.process_barrel_destruction()
        elif key == arcade.key.N and self.window:
            if self.window.width == 1200:
                self.window.set_size(2000, 1500)
            else:
                self.window.set_size(1200, 750)

    def on_key_release(self, key, modifiers):
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
        elif key == arcade.key.F:
            self.f_pressed = False

    def go_back_to_dors(self):
        #Переход к следующему уровню с сохранением очков

        if not self.controlled_entity or (self.controlled_entity and self.controlled_entity.health <= 0):
            self.show_final_window("defeat")
            return

        # Сохраняем очки в файл (только если игрок жив)
        new_total_score = self.total_score + self.level_score
        self.save_score_to_file(new_total_score)
        if self.level >= self.max_levels:
            # Останавливаем музыку перед победой
            self.stop_background_music()
            self.show_final_window("victory")
            return
        # Переходим к следующему уровню
        from dors_window import DorsView
        dors = DorsView(
            player=self.controlled_entity,  # Сохраняем игрока
            level=self.level + 1  # Увеличиваем уровень
        )

        # Останавливаем музыку перед переходом
        self.stop_background_music()

        # Переключаем View
        self.window.show_view(dors)

    def show_final_window(self, result):
        # Останавливаем музыку
        self.stop_background_music()
        # Загружаем финальные очки из файла
        final_score = self.load_score_from_file()
        if result == "victory":
            # Победа - показываем FinalWindow и очищаем файл
            self.clear_score_file()

            from final_window import FinalWindow
            final_view = FinalWindow(
                result="victory",
                score=final_score,
                levels_completed=self.level,
                total_levels=self.max_levels
            )
            self.window.show_view(final_view)
        else:
            # Поражение - показываем FinalWindow с результатом "defeat"
            from final_window import FinalWindow
            final_view = FinalWindow(
                result="defeat",
                score=final_score,
                levels_completed=max(0, self.level - 1),
                total_levels=self.max_levels
            )
            self.window.show_view(final_view)

    def on_hide_view(self):
        #Вызывается при скрытии окна (переход в другое View)
        # Останавливаем музыку при выходе с уровня
        self.stop_background_music()