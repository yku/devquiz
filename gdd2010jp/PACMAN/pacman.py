class Pacman:
    def __init__(self, x, y):
        self.c = '@'
        self.x = x
        self.y = y
    def get_pos(self): return self.x, self.y
    def move(self, x, y):
        self.x = x
        self.y = y
