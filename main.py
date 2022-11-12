import arcade
import random
from snake import Snake
from vector import Vector

WIDTH = 640
HEIGHT = 480
MAP_SIZE = (int(WIDTH / 16), int(HEIGHT / 16))
GAME_SPEED_MS = 45
GAME_SPEED = GAME_SPEED_MS / 1000

VIEW_SIGHT = 12

class MyGame(arcade.Window):
    def __init__(self, width, height, title, perf: bool = False):
        super().__init__(width, height, title)
        self.snake = Snake(5, 5)
        self.apple = Vector(random.randint(2, MAP_SIZE[0] - 2),
                            random.randint(2, MAP_SIZE[1] - 2))
        self.move_timer = 0
        self.score = 0
        self.perf = arcade.perf_graph.PerfGraph(int(WIDTH / 4), int(HEIGHT / 4))
        self.perf.center_x = int(WIDTH) - int(WIDTH / 8)
        self.perf.center_y = int(HEIGHT) - int(HEIGHT / 8)
        self.perf_enable = perf
        self.show_ray = False

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        if self.perf_enable:
            self.perf.draw()

        arcade.draw_text(f'Score: {self.score}',
                         6, HEIGHT - 24,
                         arcade.color.DUTCH_WHITE,
                         12)

        arcade.draw_rectangle_filled(self.apple.x * 16, self.apple.y * 16,
                                     16, 16, arcade.color.RED)


        if self.show_ray:
            for alpha in range(-30, 31, 15):
                line = self.snake.head + Vector(VIEW_SIGHT, 0).rotate(self.snake.cur_dir + alpha)
                vectors = bresenham(line, self.snake.head + Vector(1, 0).rotate(self.snake.cur_dir))
                flag_apple = False
                flag_tail = False
                for vec in vectors:
                    if flag_tail:
                        arcade.draw_rectangle_filled(vec[0] * 16, vec[1] * 16,
                                                     8, 8, arcade.color.BRICK_RED)
                    elif flag_apple:
                        arcade.draw_rectangle_filled(vec[0] * 16, vec[1] * 16,
                                                     8, 8, arcade.color.YELLOW)
                    else:
                        arcade.draw_rectangle_outline(vec[0] * 16, vec[1] * 16,
                                                      8, 8, arcade.color.YELLOW)
                    if Vector(vec[0], vec[1]) in self.snake.tails:
                        flag_tail = True
                    elif Vector(vec[0], vec[1]) == self.apple:
                        flag_apple = True

        arcade.draw_rectangle_filled(self.snake.head.x * 16, self.snake.head.y * 16,
                                     16, 16, arcade.color.BRIGHT_GREEN)

        for tail in self.snake.tails:
            arcade.draw_rectangle_filled(tail.x * 16, tail.y * 16,
                                         16, 16, arcade.color.GREEN)

    def on_update(self, delta_time: float):
        self.move_timer += delta_time

        self.perf.on_update(delta_time)

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

        if symbol == arcade.key.F:
            self.show_ray = not self.show_ray

        pass

    def check_bound(self, pos: Vector) -> bool:
        if 0 <= pos.x <= MAP_SIZE[0] and 0 <= pos.y <= MAP_SIZE[1]:
            return True
        return False

    def place_apple(self):
        self.apple = Vector(random.randint(2, MAP_SIZE[0] - 2),
                            random.randint(2, MAP_SIZE[1] - 2))
        while self.apple in self.snake.tails or self.apple == self.snake.head:
            self.apple = Vector(random.randint(2, MAP_SIZE[0] - 2),
                                random.randint(2, MAP_SIZE[1] - 2))

# From http://www.roguebasin.com/index.php/Bresenham%27s_Line_Algorithm#Python
def bresenham(start: Vector, end: Vector):
    """
    Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    """
    # Setup initial conditions
    start.toInt()
    end.toInt()

    # print(f'{start} ||| {end}')

    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def main():
    game = MyGame(WIDTH, HEIGHT, "Snake Game")
    game.setup()
    arcade.enable_timings()
    arcade.run()

if __name__ == "__main__":
    main()