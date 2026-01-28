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
        #Загружает случайное изображение из папки texture, исключая папку dors
        try:
            subfolders = [
                f.name for f in os.scandir(self.texture_folder)
                if f.is_dir() and f.name.lower() != "dors"
            ]

            random_folder = random.choice(subfolders)
            folder_path = os.path.join(self.texture_folder, random_folder)

            files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            random_file = random.choice(files)
            file_path = os.path.join(folder_path, random_file)

            self.background_texture = arcade.load_texture(file_path)

        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    def load_specific_background(self, folder_name):
        #Загружает фон из конкретной папки
        try:
            folder_path = os.path.join(self.texture_folder, folder_name)
            files = [f for f in os.listdir(folder_path)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            random_file = random.choice(files)
            file_path = os.path.join(folder_path, random_file)
            self.background_texture = arcade.load_texture(file_path)
        except Exception as e:
            pass

    def draw(self, width, height):
        if self.background_texture:
            arcade.draw_texture_rect(self.background_texture, arcade.LRBT(0, width, 0, height))

