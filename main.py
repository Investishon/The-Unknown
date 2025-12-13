import arcade
import os
import json
import math

# Константы
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Моя игра с редактором"
PLAYER_SCALING = 1.0
MOB_SCALING = 0.3
MOVEMENT_SPEED = 5
DEFAULT_HP = 100
DEFAULT_SPEED = 1


class Entity(arcade.Sprite):
    """Базовый класс для всех существ в игре с параметрами"""

    def __init__(self, texture_path, scale=1.0, entity_type="", entity_id=1):
        """Инициализация существа

        Args:
            texture_path (str): Путь к файлу текстуры
            scale (float): Масштаб спрайта
            entity_type (str): Тип существа ("player" или "mob")
            entity_id (int): Уникальный ID существа
        """
        super().__init__()

        self.scale = scale
        self.is_controlled = False
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.name = f"{entity_type}_{entity_id}"

        # Параметры существа
        self.max_hp = DEFAULT_HP
        self.current_hp = DEFAULT_HP
        self.speed_multiplier = DEFAULT_SPEED
        self.base_movement_speed = MOVEMENT_SPEED
        self.enti = entity_id  # ENTI параметр

        # Для инверсии изображения
        self.facing_right = True
        self.original_texture = None
        self.flipped_texture = None

        # Пытаемся загрузить текстуру из файла
        self.load_texture(texture_path)

    def load_texture(self, texture_path):
        """Загружает текстуру из файла"""
        possible_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        texture_loaded = False

        for ext in possible_extensions:
            full_path = f"{texture_path}{ext}"
            if os.path.exists(full_path):
                self.original_texture = arcade.load_texture(full_path)
                texture_loaded = True
                print(f"Загружен: {full_path}")
                break

        if not texture_loaded:
            # Создаем временную текстуру
            print(f"Файлы для {texture_path} не найдены, создаем заглушку")
            self.original_texture = self.create_temp_texture()

        # Создаем инвертированную версию текстуры
        self.create_flipped_texture()
        self.texture = self.original_texture
        self.facing_right = True

    def create_temp_texture(self):
        """Создает временную текстуру для отладки"""
        # Разные цвета для разных типов существ
        if self.entity_type == "player":
            colors = [arcade.color.BLUE, arcade.color.GREEN]
            color = colors[self.entity_id - 1] if self.entity_id - 1 < len(colors) else arcade.color.WHITE
        else:
            colors = [arcade.color.RED, arcade.color.PURPLE, arcade.color.ORANGE,
                      arcade.color.YELLOW, arcade.color.PINK]
            color = colors[self.entity_id - 1] if self.entity_id - 1 < len(colors) else arcade.color.GRAY

        # Создаем текстуру с буквой
        label = "P" if self.entity_type == "player" else "M"
        return arcade.Texture.create_filled(f"{label}{self.entity_id}", (64, 64), color)

    def create_flipped_texture(self):
        """Создает инвертированную версию текстуры"""
        # Для временных текстур просто используем оригинальную
        if "P" in self.original_texture.name or "M" in self.original_texture.name:
            self.flipped_texture = self.original_texture
        else:
            # Для настоящих текстур создаем инвертированную версию
            try:
                image = self.original_texture.image
                flipped_image = image.transpose(method=0)  # 0 = FLIP_LEFT_RIGHT
                self.flipped_texture = arcade.Texture(f"{self.original_texture.name}_flipped", flipped_image)
            except:
                self.flipped_texture = self.original_texture

    def flip_texture(self, direction):
        """Инверсия текстуры в зависимости от направления движения

        Args:
            direction (int): 1 - вправо, -1 - влево
        """
        if direction > 0 and not self.facing_right:
            # Поворачиваем вправо
            self.texture = self.original_texture
            self.facing_right = True
        elif direction < 0 and self.facing_right:
            # Поворачиваем влево
            self.texture = self.flipped_texture
            self.facing_right = False

    def update(self, delta_time: float = 1 / 60):
        """Обновление позиции существа"""
        # Рассчитываем скорость с учетом множителя
        actual_speed = self.base_movement_speed * self.speed_multiplier

        # Обновляем позицию
        self.center_x += self.change_x * actual_speed
        self.center_y += self.change_y * actual_speed

        # Инверсия текстуры при движении
        if self.change_x != 0:
            self.flip_texture(1 if self.change_x > 0 else -1)

        # Ограничиваем перемещение границами экрана
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    def get_movement_speed(self):
        """Возвращает фактическую скорость движения"""
        return self.base_movement_speed * self.speed_multiplier

    def take_damage(self, damage):
        """Нанесение урона существу"""
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp <= 0

    def heal(self, amount):
        """Лечение существа"""
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def change_scale(self, new_scale):
        """Изменение размера существа"""
        self.scale = max(0.01, new_scale)  # Минимальный размер 0.01

    def change_speed_multiplier(self, new_speed):
        """Изменение множителя скорости"""
        self.speed_multiplier = max(0.1, new_speed)  # Минимальная скорость 0.1

    def change_hp(self, new_hp):
        """Изменение максимального HP"""
        self.max_hp = max(1, new_hp)
        self.current_hp = min(self.current_hp, self.max_hp)

    def change_enti(self, new_enti):
        """Изменение параметра ENTI"""
        self.enti = new_enti

    def get_info(self):
        """Возвращает информацию о существе"""
        return {
            "name": self.name,
            "type": self.entity_type,
            "id": self.entity_id,
            "hp": f"{self.current_hp}/{self.max_hp}",
            "speed": self.speed_multiplier,
            "enti": self.enti,
            "scale": round(self.scale, 2),
            "position": (round(self.center_x), round(self.center_y)),
            "controlled": self.is_controlled
        }


class Player(Entity):
    """Класс игрока (персонажа)"""

    def __init__(self, player_id=1):
        """Инициализация игрока"""
        texture_path = f"person/person{player_id}"
        super().__init__(texture_path, PLAYER_SCALING, "player", player_id)

        # Дополнительные параметры для игроков
        self.player_id = player_id


class Mob(Entity):
    """Класс моба (монстра)"""

    def __init__(self, mob_id=1):
        """Инициализация монстра"""
        texture_path = f"mobs/mob{mob_id}"
        super().__init__(texture_path, MOB_SCALING, "mob", mob_id)

        # Дополнительные параметры для монстров
        self.mob_id = mob_id


class EditorWindow:
    """Окно редактора параметров"""

    def __init__(self, entity, close_callback):
        """Инициализация редактора

        Args:
            entity (Entity): Существо для редактирования
            close_callback (function): Функция для вызова при закрытии редактора
        """
        self.entity = entity
        self.close_callback = close_callback
        self.width = 400
        self.height = 500
        self.window = None

        # Текущие значения полей
        self.hp_value = entity.max_hp
        self.speed_value = entity.speed_multiplier
        self.enti_value = entity.enti
        self.scale_value = entity.scale

        self.create_window()

    def create_window(self):
        """Создает окно редактора"""
        self.window = arcade.Window(self.width, self.height, f"Редактор: {self.entity.name}")
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # Создаем элементы интерфейса
        self.setup()

    def setup(self):
        """Настройка элементов интерфейса редактора"""
        pass  # Элементы создаются в on_draw

    def on_draw(self):
        """Отрисовка редактора"""
        self.window.clear()

        # Заголовок
        arcade.draw_text(f"Редактор: {self.entity.name}",
                         self.width // 2, self.height - 40,
                         arcade.color.WHITE, 20, anchor_x="center")

        # Параметры
        y_offset = self.height - 100

        # HP
        arcade.draw_text(f"HP (100-1000): {self.hp_value}", 20, y_offset, arcade.color.WHITE, 16)
        arcade.draw_text("↑ W   ↓ S", 300, y_offset, arcade.color.YELLOW, 14)
        y_offset -= 40

        # Speed
        arcade.draw_text(f"Speed (0.1-5.0): {self.speed_value:.1f}", 20, y_offset, arcade.color.WHITE, 16)
        arcade.draw_text("↑ E   ↓ D", 300, y_offset, arcade.color.YELLOW, 14)
        y_offset -= 40

        # ENTI
        max_enti = 10 if self.entity.entity_type == "player" else 5
        arcade.draw_text(f"ENTI (1-{max_enti}): {self.enti_value}", 20, y_offset, arcade.color.WHITE, 16)
        arcade.draw_text("↑ R   ↓ F", 300, y_offset, arcade.color.YELLOW, 14)
        y_offset -= 40

        # Scale
        min_scale = 0.01 if self.entity.entity_type == "mob" else 0.1
        max_scale = 0.1 if self.entity.entity_type == "mob" else 5.0
        arcade.draw_text(f"Scale ({min_scale:.2f}-{max_scale:.1f}): {self.scale_value:.2f}",
                         20, y_offset, arcade.color.WHITE, 16)
        arcade.draw_text("↑ T   ↓ G", 300, y_offset, arcade.color.YELLOW, 14)
        y_offset -= 60

        # Кнопки
        arcade.draw_rectangle_filled(self.width // 2 - 80, y_offset, 150, 40, arcade.color.GREEN)
        arcade.draw_text("Применить", self.width // 2 - 80, y_offset, arcade.color.BLACK, 16, anchor_x="center")

        arcade.draw_rectangle_filled(self.width // 2 + 80, y_offset, 150, 40, arcade.color.RED)
        arcade.draw_text("Отмена", self.width // 2 + 80, y_offset, arcade.color.BLACK, 16, anchor_x="center")

        # Инструкция
        arcade.draw_text("Кликните по кнопкам или используйте клавиши",
                         20, 60, arcade.color.LIGHT_GRAY, 12)
        arcade.draw_text("Enter - применить, ESC - отмена",
                         20, 40, arcade.color.LIGHT_GRAY, 12)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш в редакторе"""
        step_small = 0.1
        step_large = 1.0

        if key == arcade.key.W:  # Увеличить HP
            self.hp_value = min(1000, self.hp_value + 10)
        elif key == arcade.key.S:  # Уменьшить HP
            self.hp_value = max(100, self.hp_value - 10)
        elif key == arcade.key.E:  # Увеличить Speed
            self.speed_value = min(5.0, self.speed_value + step_small)
        elif key == arcade.key.D:  # Уменьшить Speed
            self.speed_value = max(0.1, self.speed_value - step_small)
        elif key == arcade.key.R:  # Увеличить ENTI
            max_enti = 10 if self.entity.entity_type == "player" else 5
            self.enti_value = min(max_enti, self.enti_value + 1)
        elif key == arcade.key.F:  # Уменьшить ENTI
            self.enti_value = max(1, self.enti_value - 1)
        elif key == arcade.key.T:  # Увеличить Scale
            max_scale = 0.1 if self.entity.entity_type == "mob" else 5.0
            step = 0.01 if self.entity.entity_type == "mob" else 0.1
            self.scale_value = min(max_scale, self.scale_value + step)
        elif key == arcade.key.G:  # Уменьшить Scale
            min_scale = 0.01 if self.entity.entity_type == "mob" else 0.1
            step = 0.01 if self.entity.entity_type == "mob" else 0.1
            self.scale_value = max(min_scale, self.scale_value - step)
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            self.apply_changes()
        elif key == arcade.key.ESCAPE:
            self.close()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка кликов в редакторе"""
        button_y = 150
        button_height = 40

        # Кнопка "Применить"
        if (self.width // 2 - 80 - 75 <= x <= self.width // 2 - 80 + 75 and
                button_y - button_height // 2 <= y <= button_y + button_height // 2):
            self.apply_changes()

        # Кнопка "Отмена"
        elif (self.width // 2 + 80 - 75 <= x <= self.width // 2 + 80 + 75 and
              button_y - button_height // 2 <= y <= button_y + button_height // 2):
            self.close()

    def apply_changes(self):
        """Применяет изменения к существу"""
        self.entity.change_hp(self.hp_value)
        self.entity.change_speed_multiplier(self.speed_value)
        self.entity.change_enti(self.enti_value)
        self.entity.change_scale(self.scale_value)
        self.close()

    def close(self):
        """Закрывает редактор"""
        self.window.close()
        self.close_callback()

    def run(self):
        """Запускает редактор"""
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press
        self.window.on_mouse_press = self.on_mouse_press
        arcade.run()


class MyGame(arcade.Window):
    """Основной класс игры"""

    def __init__(self):
        """Инициализация игры"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Устанавливаем рабочий каталог на папку с игрой
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Списки для спрайтов
        self.entity_list = None
        self.controlled_entity = None

        # Управление
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Редактор
        self.editor_window = None
        self.editing_entity = None

        # Цвет фона
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # Загрузка сохраненных параметров
        self.load_entity_params()

    def load_entity_params(self):
        """Загружает сохраненные параметры существ"""
        self.entity_params = {}
        if os.path.exists("entity_params.json"):
            try:
                with open("entity_params.json", "r") as f:
                    self.entity_params = json.load(f)
                print("Параметры существ загружены")
            except:
                print("Не удалось загрузить параметры существ")

    def save_entity_params(self):
        """Сохраняет параметры всех существ"""
        params = {}
        for entity in self.entity_list:
            params[entity.name] = entity.get_info()

        try:
            with open("entity_params.json", "w") as f:
                json.dump(params, f, indent=2)
            print("Параметры существ сохранены")
        except:
            print("Не удалось сохранить параметры существ")

    def setup(self):
        """Настройка игры (создание объектов)"""

        # Создаем список всех существ
        self.entity_list = arcade.SpriteList()

        # Создаем игроков (2 персонажа)
        for i in range(1, 3):
            player = Player(i)
            player.center_x = SCREEN_WIDTH // 4 * i
            player.center_y = SCREEN_HEIGHT // 2

            # Загружаем сохраненные параметры
            player_name = f"player_{i}"
            if player_name in self.entity_params:
                params = self.entity_params[player_name]
                player.change_hp(params.get("max_hp", DEFAULT_HP))
                player.change_speed_multiplier(params.get("speed", DEFAULT_SPEED))
                player.change_enti(params.get("enti", i))
                player.change_scale(params.get("scale", PLAYER_SCALING))

            self.entity_list.append(player)

        # Первый персонаж управляемый по умолчанию
        self.controlled_entity = self.entity_list[0]
        self.controlled_entity.is_controlled = True

        # Создаем 5 монстров разных типов
        mob_positions = [
            (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 6 * 5, SCREEN_HEIGHT // 4)
        ]

        for i in range(1, 6):
            mob = Mob(i)
            mob.center_x, mob.center_y = mob_positions[i - 1]

            # Загружаем сохраненные параметры
            mob_name = f"mob_{i}"
            if mob_name in self.entity_params:
                params = self.entity_params[mob_name]
                mob.change_hp(params.get("max_hp", DEFAULT_HP))
                mob.change_speed_multiplier(params.get("speed", DEFAULT_SPEED))
                mob.change_enti(params.get("enti", i))
                mob.change_scale(params.get("scale", MOB_SCALING))

            self.entity_list.append(mob)

        print("Игра инициализирована!")
        print(f"Создано: {len([e for e in self.entity_list if isinstance(e, Player)])} персонажей")
        print(f"Создано: {len([e for e in self.entity_list if isinstance(e, Mob)])} монстров")
        print("ЛКМ - выбрать существо, ПКМ - редактор, Enter - сохранить параметры")

    def open_editor(self, entity):
        """Открывает редактор для существа"""
        self.editing_entity = entity
        self.editor_window = EditorWindow(entity, self.on_editor_closed)
        # В реальном приложении нужно было бы запустить редактор в отдельном потоке
        # Для простоты отобразим сообщение
        print(f"Редактор открыт для {entity.name}")
        print("Используйте клавиши в основном окне для редактирования:")
        print("  Q/A - HP, W/S - Speed, E/D - ENTI, R/F - Scale")
        print("  Enter - применить к этому существу")

    def on_editor_closed(self):
        """Вызывается при закрытии редактора"""
        self.editor_window = None
        self.editing_entity = None

    def on_draw(self):
        """Отрисовка экрана"""
        self.clear()

        # Рисуем всех существ
        self.entity_list.draw()

        # Подсвечиваем текущее управляемое существо
        if self.controlled_entity:
            arcade.draw_circle_outline(
                self.controlled_entity.center_x,
                self.controlled_entity.center_y,
                max(self.controlled_entity.width, self.controlled_entity.height) / 2 + 10,
                arcade.color.YELLOW,
                3
            )

        # Рисуем полоски HP
        for entity in self.entity_list:
            # Полоска HP
            bar_width = 50
            bar_height = 6
            hp_percentage = entity.current_hp / entity.max_hp

            # Фон полоски
            arcade.draw_rectangle_filled(
                entity.center_x,
                entity.center_y + entity.height / 2 + 15,
                bar_width,
                bar_height,
                arcade.color.BLACK
            )

            # Сама полоска HP
            color = arcade.color.GREEN if hp_percentage > 0.5 else arcade.color.ORANGE if hp_percentage > 0.2 else arcade.color.RED
            arcade.draw_rectangle_filled(
                entity.center_x - bar_width / 2 + (bar_width * hp_percentage) / 2,
                entity.center_y + entity.height / 2 + 15,
                bar_width * hp_percentage,
                bar_height,
                color
            )

            # Имя и параметры под существом
            info_y = entity.center_y - entity.height / 2 - 20
            arcade.draw_text(
                f"{entity.name}",
                entity.center_x, info_y,
                arcade.color.WHITE, 10,
                anchor_x="center"
            )

            # Если это редактируемое существо, показываем его параметры
            if entity == self.editing_entity:
                arcade.draw_text(
                    f"HP: {entity.max_hp} SPD: {entity.speed_multiplier:.1f}",
                    entity.center_x, info_y - 15,
                    arcade.color.YELLOW, 10,
                    anchor_x="center"
                )
                arcade.draw_text(
                    f"ENTI: {entity.enti} SCL: {entity.scale:.2f}",
                    entity.center_x, info_y - 30,
                    arcade.color.YELLOW, 10,
                    anchor_x="center"
                )

        # Отображаем информацию
        arcade.draw_text(f"Управление: {self.controlled_entity.name} (WASD или стрелки)",
                         10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)
        arcade.draw_text("ЛКМ - выбрать, ПКМ - редактор, Enter - сохранить всё",
                         10, SCREEN_HEIGHT - 50, arcade.color.WHITE, 14)
        arcade.draw_text("Q/A-HP, W/S-Speed, E/D-ENTI, R/F-Scale (при редактировании)",
                         10, SCREEN_HEIGHT - 70, arcade.color.WHITE, 14)
        arcade.draw_text("ESC - выход", 10, SCREEN_HEIGHT - 90, arcade.color.WHITE, 14)

        # Показываем, кто сейчас под контролем
        controlled_info = self.controlled_entity.get_info()
        info_text = (f"Управляем: {controlled_info['name']} | "
                     f"HP: {controlled_info['hp']} | "
                     f"Speed: {controlled_info['speed']:.1f} | "
                     f"ENTI: {controlled_info['enti']} | "
                     f"Scale: {controlled_info['scale']:.2f}")

        arcade.draw_text(info_text,
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30,
                         arcade.color.CYAN, 14, anchor_x="center")

        # Если есть редактируемое существо
        if self.editing_entity and self.editing_entity != self.controlled_entity:
            editing_info = self.editing_entity.get_info()
            edit_text = (f"Редактируем: {editing_info['name']} | "
                         f"HP: {self.editing_entity.max_hp} | "
                         f"Speed: {self.editing_entity.speed_multiplier:.1f} | "
                         f"ENTI: {self.editing_entity.enti} | "
                         f"Scale: {self.editing_entity.scale:.2f}")

            arcade.draw_text(edit_text,
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50,
                             arcade.color.YELLOW, 14, anchor_x="center")

    def on_update(self, delta_time):
        """Обновление логики игры"""

        if self.controlled_entity:
            # Обновляем движение управляемого существа
            self.controlled_entity.change_x = 0
            self.controlled_entity.change_y = 0

            if self.up_pressed and not self.down_pressed:
                self.controlled_entity.change_y = 1
            elif self.down_pressed and not self.up_pressed:
                self.controlled_entity.change_y = -1

            if self.left_pressed and not self.right_pressed:
                self.controlled_entity.change_x = -1
            elif self.right_pressed and not self.left_pressed:
                self.controlled_entity.change_x = 1

        # Обновляем все существа
        self.entity_list.update(delta_time)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""

        # Управление WASD или стрелками
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True

        # Редактирование параметров (если есть редактируемое существо)
        elif self.editing_entity:
            if key == arcade.key.Q:  # Увеличить HP
                self.editing_entity.change_hp(self.editing_entity.max_hp + 10)
            elif key == arcade.key.A:  # Уменьшить HP
                self.editing_entity.change_hp(max(1, self.editing_entity.max_hp - 10))
            elif key == arcade.key.W:  # Увеличить Speed
                self.editing_entity.change_speed_multiplier(self.editing_entity.speed_multiplier + 0.1)
            elif key == arcade.key.S:  # Уменьшить Speed
                self.editing_entity.change_speed_multiplier(max(0.1, self.editing_entity.speed_multiplier - 0.1))
            elif key == arcade.key.E:  # Увеличить ENTI
                max_enti = 10 if self.editing_entity.entity_type == "player" else 5
                self.editing_entity.change_enti(min(max_enti, self.editing_entity.enti + 1))
            elif key == arcade.key.D:  # Уменьшить ENTI
                self.editing_entity.change_enti(max(1, self.editing_entity.enti - 1))
            elif key == arcade.key.R:  # Увеличить Scale
                max_scale = 0.1 if self.editing_entity.entity_type == "mob" else 5.0
                step = 0.01 if self.editing_entity.entity_type == "mob" else 0.1
                self.editing_entity.change_scale(min(max_scale, self.editing_entity.scale + step))
            elif key == arcade.key.F:  # Уменьшить Scale
                min_scale = 0.01 if self.editing_entity.entity_type == "mob" else 0.1
                step = 0.01 if self.editing_entity.entity_type == "mob" else 0.1
                self.editing_entity.change_scale(max(min_scale, self.editing_entity.scale - step))
            elif key == arcade.key.ENTER or key == arcade.key.RETURN:
                # Применить изменения только к редактируемому существу
                print(f"Параметры {self.editing_entity.name} сохранены")
                self.editing_entity = None

        # Сохранение всех параметров
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            self.save_entity_params()
            print("Все параметры сохранены в entity_params.json")

        # Выход из игры
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""

        # Управление WASD или стрелками
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышкой"""
        clicked_entities = arcade.get_sprites_at_point((x, y), self.entity_list)

        if clicked_entities:
            entity = clicked_entities[0]

            if button == arcade.MOUSE_BUTTON_LEFT:
                # ЛКМ - выбрать для управления
                if entity != self.controlled_entity:
                    if self.controlled_entity:
                        self.controlled_entity.is_controlled = False

                    entity.is_controlled = True
                    self.controlled_entity = entity

                    print(f"Теперь управляем: {entity.name}")

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                # ПКМ - открыть редактор
                self.open_editor(entity)
                print(f"Редактируем: {entity.name}")
                print("Используйте Q/A, W/S, E/D, R/F для изменения параметров")
                print("Enter - применить изменения к этому существу")


def create_dummy_images():
    """Создает заглушки для изображений, если их нет"""
    os.makedirs("person", exist_ok=True)
    os.makedirs("mobs", exist_ok=True)

    print("Папки созданы: person/, mobs/")
    print("Положите ваши JPG изображения в эти папки:")


def main():
    """Главная функция для запуска игры"""

    # Проверяем наличие папок
    if not os.path.exists("person") or not os.path.exists("mobs"):
        create_dummy_images()

    # Создаем окно игры
    window = MyGame()

    # Настраиваем игру
    window.setup()

    # Запускаем игровой цикл
    arcade.run()


if __name__ == "__main__":
    main()