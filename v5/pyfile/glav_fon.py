import os
import random
import arcade

class BackgroundManager:
    def __init__(self, texture_folder="../texture"):
        self.texture_folder = texture_folder
        self.background_texture = None
        # НЕ загружаем случайный фон автоматически
        # self.load_random_background()

    def load_random_background(self):
        """Загружает случайное изображение из папки texture, исключая папку dors"""
        try:
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

    def load_specific_background(self, folder_name):
        """Загружает фон из конкретной папки"""
        try:
            folder_path = os.path.join(self.texture_folder, folder_name)

            if not os.path.exists(folder_path):
                print(f"Папка {folder_path} не найдена")
                return

            files = [f for f in os.listdir(folder_path)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if not files:
                print(f"В папке {folder_name} нет изображений")
                return

            random_file = random.choice(files)
            file_path = os.path.join(folder_path, random_file)

            self.background_texture = arcade.load_texture(file_path)
            print(f"Загружен фон: {folder_name}/{random_file}")

        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")

    def draw(self, width, height):
        if self.background_texture:
            arcade.draw_texture_rect(self.background_texture, arcade.LRBT(0, width, 0, height))

