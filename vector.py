from math import sqrt, cos, sin, radians

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return sqrt((self.x * self.x) + (self.y * self.y))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{self.x}, {self.y}'

    def rotate(self, angle: int):
        alpha = radians(angle)
        return Vector(self.x * cos(alpha) - self.y * sin(alpha), self.x * sin(alpha) + self.y * cos(alpha))