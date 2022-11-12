import arcade
import random
from snake import Snake
from vector import Vector

WIDTH = 640
HEIGHT = 480
MAP_SIZE = (int(WIDTH / 16), int(HEIGHT / 16))

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.snake = Snake(5, 5)
        self.move_timer = 0

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(self.snake.head.x * 16, self.snake.head.y * 16,
                                     16, 16, arcade.color.WHITE)
        for tail in self.snake.tails:
            arcade.draw_rectangle_filled(tail.x * 16, tail.y * 16,
                                         16, 16, arcade.color.WHITE)

    def on_update(self, delta_time: float):
        self.move_timer += delta_time

        if self.move_timer >= 0.1:
            self.snake.move_forward()
            self.snake.cut_tail()
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


def main():
    game = MyGame(640, 480, "Snake Game")
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()