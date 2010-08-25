#!/usr/bin/python
import strategy
from defines import *

class Character:
    def __init__(self, map, x, y):
        self.map = map
        self.x = self.prev_x = x
        self.y = self.prev_y = y
    
    def move(self):
        assert False

class Pacman(Character):
    def __init__(self, map, x, y):
        Character.__init__(self, map, x, y)
        self.history = ""

    def up(self):
        self.map.set(self.x, self.y, ' ')
        self.prev_x = self.x
        self.prev_y = self.y
        self.y -= 1
        self.get_dot()
    def down(self):
        self.map.set(self.x, self.y, ' ')
        self.prev_x = self.x
        self.prev_y = self.y
        self.y += 1
        self.get_dot()
    def right(self):
        self.map.set(self.x, self.y, ' ')
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += 1
        self.get_dot()
    def left(self):
        self.map.set(self.x, self.y, ' ')
        self.prev_x = self.x
        self.prev_y = self.y
        self.x -= 1
        self.get_dot()

    def get_dot(self):
        for dot in self.map.dots:
            if dot.x == self.x and dot.y == self.y and dot.exist:
                dot.exist = False
                self.map.point += 1

    def update(self):
        self.map.set(self.x, self.y, '@')

class Enemy(Character):
    def __init__(self, map, x, y):
        Character.__init__(self, map, x, y)
        self.face = ""
    def first_move(self):
        self.f = strategy.first
        self.f(self)

    def up(self):
        self.dir = UP
        self.prev_x = self.x
        self.prev_y = self.y
        self.y -= 1
    
    def down(self):
        self.dir = DOWN
        self.prev_x = self.x
        self.prev_y = self.y
        self.y += 1
    
    def left(self):
        self.dir = LEFT
        self.prev_x = self.x
        self.prev_y = self.y
        self.x -= 1
    
    def right(self):
        self.dir = RIGHT
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += 1
    
    def update(self):
        self.map.set(self.prev_x, self.prev_y, ' ')
        for dot in self.map.dots:
            if dot.x == self.prev_x and dot.y == self.prev_y:
                if dot.exist: self.map.set(self.prev_x, self.prev_y, '.')
                else: self.map.set(self.prev_x, self.prev_y, ' ')
        self.map.set(self.x, self.y, self.face)

class EnemyV(Enemy):
    def __init__(self, map, x, y):
        Enemy.__init__(self, map, x, y)
        self.face = 'V'
    def move(self):
        ways = self.map.get_way(self)
        if   ways == 1: self.f = strategy.one_way
        elif ways == 2: self.f = strategy.two_way
        else:           self.f = strategy.v 
        self.f(self)

class EnemyH(Enemy):
    def __init__(self, map, x, y):
        Enemy.__init__(self, map, x, y)
        self.face = 'H'
    def move(self):
        ways = self.map.get_way(self)
        if   ways == 1: self.f = strategy.one_way
        elif ways == 2: self.f = strategy.two_way
        else:           self.f = strategy.h 
        self.f(self)

class EnemyL(Enemy):
    def __init__(self, map, x, y):
        Enemy.__init__(self, map, x, y)
        self.face = 'L'
    def move(self):
        ways = self.map.get_way(self)
        if   ways == 1: self.f = strategy.one_way
        elif ways == 2: self.f = strategy.two_way
        else:           self.f = strategy.l 
        self.f(self)

class EnemyR(Enemy):
    def __init__(self, map, x, y):
        Enemy.__init__(self, map, x, y)
        self.face = 'R'
    def move(self):
        ways = self.map.get_way(self)
        if   ways == 1: self.f = strategy.one_way
        elif ways == 2: self.f = strategy.two_way
        else:           self.f = strategy.r 
        self.f(self)

class EnemyJ(Enemy):
    def __init__(self, map, x, y):
        Enemy.__init__(self, map, x, y)
        self.face = 'J'
        self.mode = ''
    def move(self):
        ways = self.map.get_way(self)
        if   ways == 1: self.f = strategy.one_way
        elif ways == 2: self.f = strategy.two_way
        else:
            if self.mode == '' or self.mode == 'R': self.mode = 'L'
            else: self.mode = 'R'
            self.f = strategy.j 
        self.f(self)
