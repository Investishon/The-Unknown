# Создай файл create_dust_texture.py:
import arcade
import random

# Создаем окно
window = arcade.Window(16, 16, "Dust Texture Creator")

# Создаем спрайт лист
sprite_list = arcade.SpriteList()

# Создаем несколько случайных пикселей
for _ in range(10):
    sprite = arcade.SpriteSolidColor(1, 1, (220, 220, 220, 100))
    sprite.center_x = random.randint(0, 16)
    sprite.center_y = random.randint(0, 16)
    sprite_list.append(sprite)

# Сохраняем текстуру
sprite_list.draw()
arcade.get_image().save("texture/pred/dust.png")

