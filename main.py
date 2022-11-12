import arcade
import random
from snake import Snake
from vector import Vector

WIDTH = 640
HEIGHT = 480
MAP_SIZE = (int(WIDTH / 16), int(HEIGHT / 16))
GAME_SPEED_MS = 75
GAME_SPEED = GAME_SPEED_MS / 1000

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.snake = Snake(5, 5)
        self.apple = Vector(random.randint(2, MAP_SIZE[0] - 2),
                            random.randint(2, MAP_SIZE[1] - 2))
        self.move_timer = 0
        self.score = 0

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        arcade.draw_text(f'Score: {self.score}',
                         6, HEIGHT - 24,
                         arcade.color.DUTCH_WHITE,
                         12)

        arcade.draw_rectangle_filled(self.apple.x * 16, self.apple.y * 16,
                                     16, 16, arcade.color.RED)

        arcade.draw_rectangle_filled(self.snake.head.x * 16, self.snake.head.y * 16,
                                     16, 16, arcade.color.BRIGHT_GREEN)
        for tail in self.snake.tails:
            arcade.draw_rectangle_filled(tail.x * 16, tail.y * 16,
                                         16, 16, arcade.color.GREEN)

    def on_update(self, delta_time: float):
        self.move_timer += delta_time

        if self.move_timer >= GAME_SPEED:
            if not self.snake.move_forward() or not self.check_bound(self.snake.head):
                # Todo GameOver Screen
                arcade.exit()
            if self.snake.head != self.apple:
                self.snake.cut_tail()
            else:
                self.score += 1
                self.place_apple()
            self.move_timer = 0

        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if (symbol == arcade.key.W or symbol == arcade.key.UP) and self.snake.cur_dir != 270:
            self.snake.next_dir = 90
        elif (symbol == arcade.key.A or symbol == arcade.key.LEFT) and self.snake.cur_dir != 0:
            self.snake.next_dir = 180
        elif (symbol == arcade.key.S or symbol == arcade.key.DOWN) and self.snake.cur_dir != 90:
            self.snake.next_dir = 270
        elif (symbol == arcade.key.D or symbol == arcade.key.RIGHT) and self.snake.cur_dir != 180:
            self.snake.next_dir = 0
        pass

    def check_bound(self, pos: Vector) -> bool:
        if 0 <= pos.x <= MAP_SIZE[0] and 0 <= pos.y <= MAP_SIZE[1]:
            return True
        return False

    def place_apple(self):
        self.apple = Vector(random.randint(2, MAP_SIZE[0] - 2),
                            random.randint(2, MAP_SIZE[1] - 2))

def main():
    game = MyGame(WIDTH, HEIGHT, "Snake Game")
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()