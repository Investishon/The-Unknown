import arcade
from pyglet.graphics import Batch

SCREEN_WIDTH = 1220
SCREEN_HEIGHT = 850
SCREEN_TITLE = "Аркадный Бегун"
PLAYER_SPEED = 5
GRAVITY = 0.5


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        # Спрайт игрока
        self.player = arcade.Sprite(
            ":resources:/images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            scale=0.5)
        self.tile_map = arcade.load_tilemap(
            ":resources:/tiled_maps/level_1.json",
            scaling=0.5)
        self.center_x = 100
        self.center_y = 100# Во встроенных ресурсах есть даже уровни!
        self.player_spritelist = ...
        self.coin_list = self.scene['Coins']
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.coin_list = self.scene['Coins']
        self.score = 0
        self.batch = Batch()

        # Физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene['Platforms'])
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.player, self.scene['Bombs'])

    def on_draw(self):
        self.clear()
        self.player_spritelist.draw()
        self.scene.draw()
        self.batch.draw()

    def on_update(self, delta_time):
        ...

        self.text = arcade.Text(f'Score: {self.score}',
                                10, self.height - 30, arcade.color.WHITE,
                                24, batch=self.batch)

    def on_key_press(self, key, modifiers):
        ...

    def on_key_release(self, key, modifiers):
        ...


def setup_game(width=1220, height=850, title="Аркадный Бегун"):
    game = MyGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()