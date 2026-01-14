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
        # СОЗДАЕМ ОДНО ОКНО - и больше нигде не создаем!
        window = arcade.Window(800, 600, "The Unknown")
        window.show_view(StartWindow())
        arcade.run()  # ← ТОЛЬКО ОДИН arcade.run() во всей программе!

except ImportError as e:
    print(f"Не удалось загрузить меню из v2: {e}")
    print("Запускаю старую версию игры...")

    # Запасной вариант: запуск старой игры
    # НО И ЗДЕСЬ ТОЖЕ ОДНО ОКНО!
    from dors_window import DorsWindow

    def main():
        window = arcade.Window(1200, 750, "The Unknown")  # ← Изменено с 800x600 на 1200x750
        window.show_view(StartWindow())
        arcade.run()

if __name__ == "__main__":
    main()