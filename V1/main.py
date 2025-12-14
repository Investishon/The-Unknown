import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Моя игра"


class Entity(arcade.Sprite):
    def __init__(self, image_path, scale=0.9):
        super().__init__(image_path, scale)
        self.is_controlled = False


class Player(Entity):
    def __init__(self, player_id):
        super().__init__(f"V1/person/person{player_id}.jpg", 1.0)


class Mob(Entity):
    def __init__(self, mob_id):
        super().__init__(f"V1/mobs/mob{mob_id}.jpg", 0.5)  # В 50 раз меньше


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.all_entities = None
        self.controlled_entity = None
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.all_entities = arcade.SpriteList()

        # 2 персонажа
        for i in range(1, 3):
            player = Player(i)
            player.center_x = 200 + (i - 1) * 300
            player.center_y = 300
            self.all_entities.append(player)

        # 5 монстров
        for i in range(1, 6):
            mob = Mob(i)
            mob.center_x = 100 + (i - 1) * 140
            mob.center_y = 100
            self.all_entities.append(mob)

        self.controlled_entity = self.all_entities[0]
        self.controlled_entity.is_controlled = True

    def on_draw(self):
        self.clear()
        self.all_entities.draw()

        if self.controlled_entity:
            arcade.draw_circle_outline(
                self.controlled_entity.center_x,
                self.controlled_entity.center_y,
                30,
                arcade.color.YELLOW,
                3
            )
        info_text = arcade.Text(
            "Управление: WASD | Кликните на существо для управления",
            10, 570,
            arcade.color.WHITE, 14
        )
        info_text.draw()

    def on_update(self, delta_time):
        if self.controlled_entity:
            # Обнуляем движение
            self.controlled_entity.change_x = 0
            self.controlled_entity.change_y = 0

            # Применяем управление
            if self.w_pressed:
                self.controlled_entity.change_y = 5
            if self.s_pressed:
                self.controlled_entity.change_y = -5
            if self.a_pressed:
                self.controlled_entity.change_x = -5
            if self.d_pressed:
                self.controlled_entity.change_x = 5

            # Обновляем позицию
            self.controlled_entity.center_x += self.controlled_entity.change_x
            self.controlled_entity.center_y += self.controlled_entity.change_y

            # Ограничение движения
            if self.controlled_entity.left < 0:
                self.controlled_entity.left = 0
            if self.controlled_entity.right > SCREEN_WIDTH:
                self.controlled_entity.right = SCREEN_WIDTH
            if self.controlled_entity.bottom < 0:
                self.controlled_entity.bottom = 0
            if self.controlled_entity.top > SCREEN_HEIGHT:
                self.controlled_entity.top = SCREEN_HEIGHT

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            clicked = arcade.get_sprites_at_point((x, y), self.all_entities)
            if clicked:
                new_entity = clicked[0]
                if new_entity != self.controlled_entity:
                    self.controlled_entity.is_controlled = False
                    new_entity.is_controlled = True
                    self.controlled_entity = new_entity


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()