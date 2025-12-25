import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from V2.start_window import StartWindow

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_screen = StartWindow()
    window.show_view(start_screen)
    arcade.run()

if __name__ == "__main__":
    main()