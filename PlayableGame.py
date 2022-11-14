import arcade
import random
import pickle
from snake import Snake
from vector import Vector
from SimGame import SimData, MapData

class PlayableGame(arcade.Window):
    def __init__(self, width, height, title,
                 perf: bool = False,
                 view_sight: int = 12,
                 game_speed: int = 75,
                 record: bool = False,
                 record_filename: str = "record.simData"):
        super().__init__(width, height, title)
        self.WIDTH = width
        self.HEIGHT = height
        self.MAP_SIZE = (int(self.WIDTH / 16), int(self.HEIGHT / 16))

        self.game_speed = game_speed / 1000
        self.view_sight = view_sight

        self.snake = Snake(5, 5)
        self.apple = Vector(random.randint(2, self.MAP_SIZE[0] - 2),
                            random.randint(2, self.MAP_SIZE[1] - 2))
        self.move_timer = 0
        self.score = 0
        self.perf = arcade.perf_graph.PerfGraph(int(self.WIDTH / 4), int(self.HEIGHT / 4))
        self.perf.center_x = int(self.WIDTH) - int(self.WIDTH / 8)
        self.perf.center_y = int(self.HEIGHT) - int(self.HEIGHT / 8)
        self.perf_enable = perf
        self.show_ray = False
        self.show_view_box = False
        self.view_box = []
        for x in range(1, self.view_sight + 1):
            for y in range(-3 - int(x / 4), 4 + int(x / 4)):
                self.view_box.append(Vector(x, y))
        self.record = record
        self.simData = SimData(width, height)
        self.record_filename = record_filename

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        if self.perf_enable:
            self.perf.draw()

        arcade.draw_text(f'Score: {self.score}',
                         6, self.HEIGHT - 24,
                         arcade.color.DUTCH_WHITE,
                         12)

        arcade.draw_rectangle_filled(self.apple.x * 16, self.apple.y * 16,
                                     16, 16, arcade.color.RED)


        if self.show_view_box:
            line = []
            for vec in self.view_box:
                box = self.snake.head + vec.rotate(self.snake.cur_dir)
                box.toInt()
                if box == self.apple:
                    line = bresenham(self.snake.head + Vector(1, 0).rotate(self.snake.cur_dir), self.apple)
                arcade.draw_rectangle_outline(box.x * 16, box.y * 16,
                                              8, 8, arcade.color.YELLOW)
            for vec in line:
                arcade.draw_rectangle_filled(vec[0] * 16, vec[1] * 16,
                                             8, 8, arcade.color.YELLOW)

        if self.show_ray:
            for alpha in range(-30, 31, 15):
                line = self.snake.head + Vector(self.view_sight, 0).rotate(self.snake.cur_dir + alpha)
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

        if self.move_timer >= self.game_speed:
            if self.record:
                self.simData.addData(MapData(self.snake, self.apple))
            if not self.snake.move_forward() or not check_bound(self.snake.head, self.MAP_SIZE):
                # Todo GameOver Screen
                if self.record:
                    with open(self.record_filename, "wb") as file:
                        pickle.dump(self.simData, file)
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
            if self.show_ray:
                self.show_view_box = False

        if symbol == arcade.key.G:
            self.show_view_box = not self.show_view_box
            if self.show_view_box:
                self.show_ray = False

        pass

    def place_apple(self):
        self.apple = Vector(random.randint(2, self.MAP_SIZE[0] - 2),
                            random.randint(2, self.MAP_SIZE[1] - 2))
        while self.apple in self.snake.tails or self.apple == self.snake.head:
            self.apple = Vector(random.randint(2, self.MAP_SIZE[0] - 2),
                                random.randint(2, self.MAP_SIZE[1] - 2))

def check_bound(pos: Vector, size) -> bool:
    if 0 <= pos.x <= size[0] and 0 <= pos.y <= size[1]:
        return True
    return False

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