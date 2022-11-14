import arcade
import pickle
from snake import Snake
from vector import Vector
import os
import copy

class MapData:
    def __init__(self, snake: Snake, apple: Vector):
        self.snake = copy.copy(snake)
        self.apple = copy.copy(apple)

class SimData:
    def __init__(self, WIDTH, HEIGHT):
        self.data = []
        self.width = WIDTH
        self.height = HEIGHT

    def addData(self, data: MapData):
        self.data.append(data)

    def getLen(self):
        return len(self.data)

class SimGame(arcade.Window):
    def __init__(self, filename, game_speed: int = 100):
        self.simData: SimData
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.simData = pickle.load(file)
        super().__init__(self.simData.width, self.simData.height, "Sim")
        self.move_timer = 0
        self.score = 0
        self.game_speed = game_speed / 1000
        self.simIndex = 0

    def on_draw(self):
        self.clear()
        to_draw = self.simData.data[self.simIndex]

        arcade.draw_rectangle_filled(to_draw.apple.x * 16, to_draw.apple.y * 16,
                                     16, 16, arcade.color.RED)

        arcade.draw_rectangle_filled(to_draw.snake.head.x * 16, to_draw.snake.head.y * 16,
                                     16, 16, arcade.color.BRIGHT_GREEN)

        for tail in to_draw.snake.tails:
            arcade.draw_rectangle_filled(tail.x * 16, tail.y * 16,
                                         16, 16, arcade.color.GREEN)

    def on_update(self, delta_time: float):
        self.move_timer += delta_time

        if self.move_timer >= self.game_speed:
            self.simIndex += 1
            if self.simIndex == self.simData.getLen():
                arcade.exit()
            self.move_timer = 0

