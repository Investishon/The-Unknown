import os
import random
import arcade


class BackgroundManager:
    def __init__(self, texture_folder="../texture"):
        self.texture_folder = texture_folder
        self.background_texture = None
        self.load_random_background()

    def load_random_background(self):
        """Загружает случайное изображение из папки texture, исключая папку dors"""
        try:
            # Получаем все папки, исключая "dors"
            subfolders = [
                f.name for f in os.scandir(self.texture_folder)
                if f.is_dir() and f.name.lower() != "dors"
            ]

            if not subfolders:
                print(f"В папке {self.texture_folder} нет подходящих подпапок (dors исключена)")
                return

            random_folder = random.choice(subfolders)
            folder_path = os.path.join(self.texture_folder, random_folder)

            files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if not files:
                print(f"В папке {random_folder} нет изображений")
                return

            random_file = random.choice(files)
            file_path = os.path.join(folder_path, random_file)

            self.background_texture = arcade.load_texture(file_path)

            print(f"Загружен фон: {random_folder}/{random_file}")

        except FileNotFoundError:
            print(f"Папка {self.texture_folder} не найдена")
        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")

    def draw(self, width, height):
        """Отрисовывает фон на весь экран"""
        if self.background_texture:
            # Вариант 1: Используем XYWH (x, y, width, height)
            rect = arcade.XYWH(0, 0, width, height)
            arcade.draw_texture_rect(self.background_texture, rect)
