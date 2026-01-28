import arcade
from start_window import StartWindow


def main():
    window = arcade.Window(800, 600, "The Unknown")
    window.show_view(StartWindow())
    arcade.run()

main()