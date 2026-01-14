import arcade
import sys
import os

# Получаем путь к папке v2
current_dir = os.path.dirname(os.path.abspath(__file__))  # pyfile/
parent_dir = os.path.dirname(current_dir)  # v5/
v2_path = os.path.join(parent_dir, "v2")

# Добавляем путь к v2 для импорта меню
sys.path.insert(0, v2_path)

try:
    from start_window import StartWindow


    def main():
        """Запускает игру через новое меню"""
        window = arcade.Window(800, 600, "The Unknown")
        window.show_view(StartWindow())
        arcade.run()

except ImportError as e:
    print(f"Не удалось загрузить меню из v2: {e}")
    print("Запускаю старую версию игры...")

    # Запасной вариант: запуск старой игры
    from dors_window import DorsWindow


    def main():
        window = DorsWindow()
        arcade.run()

if __name__ == "__main__":
    main()