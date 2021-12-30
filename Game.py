import pygame.time
import random

from Snake import Snake


class GameManager:
    def __init__(self, mapsize, blocksize):
        self._fpsCap = 60
        self._mapSize = mapsize
        self._blockSize = blocksize
        self._gameClock = pygame.time.Clock()
        self.gameOver = False
        self.gameSpeed = 0.25
        self._snake = Snake()
        self._applePos = (
            random.randint(1, self._mapSize[0] - 2),
            random.randint(1, self._mapSize[1] - 2)
        )
        self.score = 0
        return

    def tick(self):
        return self._gameClock.tick(self._fpsCap)

    def set_fps(self, fpscap):
        self._fpsCap = fpscap
        return

    def update(self):
        self.gameOver = not self._snake.move()

        snake_head = self._snake.positions[-1]
        if snake_head[0] < 0 or snake_head[0] > self._mapSize[0]:
            self.gameOver = True
            return
        if snake_head[1] < 0 or snake_head[1] > self._mapSize[1]:
            self.gameOver = True
            return

        if snake_head == self._applePos:
            self.score += 1
            self._snake.grow()
            self._applePos = (
                random.randint(1, self._mapSize[0] - 2),
                random.randint(1, self._mapSize[1] - 2)
            )

            while self._applePos in self._snake.positions:
                self._applePos = (
                    random.randint(1, self._mapSize[0] - 2),
                    random.randint(1, self._mapSize[1] - 2)
                )
            self.gameSpeed -= 0.01
            if self.gameSpeed < 0.01:
                self.gameSpeed = 0.01

        return

    def draw(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        for snakePos in self._snake.positions:
            screen.fill((0, 255, 0), (snakePos[0] * self._blockSize,
                                      snakePos[1] * self._blockSize,
                                      self._blockSize,
                                      self._blockSize))
        screen.fill((255, 0, 0), (self._applePos[0] * self._blockSize,
                                  self._applePos[1] * self._blockSize,
                                  self._blockSize,
                                  self._blockSize))

        return

    def turn_snake(self, direction):
        if direction[0] == self._snake.direction[0] or direction[1] == self._snake.direction[1]:
            return
        self._snake.direction = direction
        return

    def set_speed(self):
        return
