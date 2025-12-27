import arcade
import sys
import os

# Получаем путь к папке V2
current_dir = os.path.dirname(os.path.abspath(__file__))  # PyFile/
parent_dir = os.path.dirname(current_dir)  # V5/
v2_path = os.path.join(parent_dir, "V2")

# Добавляем путь к V2 для импорта меню
sys.path.insert(0, v2_path)

try:
    from start_window import StartWindow


    def main():
        """Запускает игру через новое меню"""
        window = arcade.Window(800, 600, "The Unknown")
        window.show_view(StartWindow())
        arcade.run()

except ImportError as e:
    print(f"Не удалось загрузить меню из V2: {e}")
    print("Запускаю старую версию игры...")

    # Запасной вариант: запуск старой игры
    from Dors_window import DorsWindow


    def main():
        window = DorsWindow()
        arcade.run()

if __name__ == "__main__":
    main()