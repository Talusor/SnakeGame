
class Snake:
    def __init__(self):
        self.positions = [(0, 0), (1, 0), (2, 0)]
        self.tailPosition = (0, 0)
        self.direction = [1, 0]
        return

    def move(self):
        head = self.positions[-1]
        self.tailPosition = self.positions[0]

        if (head[0] + self.direction[0], head[1] + self.direction[1]) == self.positions[-2]:
            self.direction[0] = self.direction[0] * -1
            self.direction[1] = self.direction[1] * -1

        for i in range(len(self.positions) - 1):
            self.positions[i] = self.positions[i + 1]
        self.positions[-1] = (head[0] + self.direction[0], head[1] + self.direction[1])
        if self.positions[-1] in self.positions[:-1]:
            return False
        return True

    def grow(self):
        self.positions = [self.tailPosition] + self.positions
        return
