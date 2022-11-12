from vector import Vector

class Snake:
    def __init__(self, startX, startY):
        self.unitVec = Vector(1, 0)
        self.head = Vector(startX, startY)
        self.tails = [self.head - Vector(2, 0), self.head - Vector(1, 0)]
        self.cur_dir = 0
        self.next_dir = 0

    def move_forward(self):
        self.tails.append(self.head)
        self.head += self.unitVec.rotate(self.next_dir)
        self.cur_dir = self.next_dir

    def cut_tail(self):
        self.tails = self.tails[1:]