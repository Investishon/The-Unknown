import arcade


def main():
    #Запускает игру в едином окне"
    window = arcade.Window(1200, 750, "The Unknown", resizable=True)

    # Начинаем с меню или с dors
    try:
        from start_window import StartWindow
        window.show_view(StartWindow())
    except ImportError:
        from dors_window import DorsView
        window.show_view(DorsView())

    arcade.run()


if __name__ == "__main__":
    main()