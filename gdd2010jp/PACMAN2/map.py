#!/usr/bin/python
from character import *
from defines import *

class Map:
    def __init__(self):
        self.w = self.h = 0
        self.time = self.cur_time = int(0)
        self.point = int(0)
        self.enemies = []
        self.dots = []

    def generate(self, filename):
        f = open(filename)
        self.time = int(f.readline())
        w, h = f.readline().split(' ')
        self.w = int(w)
        self.h = int(h)
        self.field = [0 for i in xrange(self.w * self.h)]
        x, y = 0, 0
        for c in f.read():
            if c == '\n':
                x = 0
                y += 1
                continue
            self.field[y * self.w + x] = c
            x += 1
        self.gen_objects()
    
    def gen_objects(self):
        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                c = self.get(x, y)
                if c == '@':
                    self.pacman = Pacman(self, x, y)
                elif c == 'V':
                    self.enemies.append(EnemyV(self, x, y))
                elif c == 'H':
                    self.enemies.append(EnemyH(self, x, y))
                elif c == 'L':
                    self.enemies.append(EnemyL(self, x, y))
                elif c == 'R':
                    self.enemies.append(EnemyR(self, x, y))
                elif c == 'J':
                    self.enemies.append(EnemyJ(self, x, y))
                elif c == '.':
                    self.dots.append(Dot(self, x, y))
                x += 1

    def get(self, x, y):
        return self.field[y * self.w + x]
    
    def set(self, x, y, val):
        self.field[y * self.w + x] = val
    
    def input(self):
        for e in self.enemies:
            if self.cur_time == 0: e.first_move()
            else: e.move()

        while 1:
            key = raw_input()
            if   key == 'h' and self.is_dir(self.pacman, LEFT):
                self.pacman.left()
                break
            elif key == 'j' and self.is_dir(self.pacman, DOWN):
                self.pacman.down()
                break
            elif key == 'k' and self.is_dir(self.pacman, UP):
                self.pacman.up()
                break
            elif key == 'l' and self.is_dir(self.pacman, RIGHT):
                self.pacman.right()
                break
            elif key == 'q': exit() 

        for e in self.enemies:
            e.update()
        self.pacman.update()

    def is_dir(self, chara, dir):
        x, y = chara.x, chara.y
        if   dir == UP:    y -= 1
        elif dir == DOWN:  y += 1 
        elif dir == LEFT:  x -= 1
        elif dir == RIGHT: x += 1 
        
        if self.get(x, y) == '#': return False
        else: return True
    
    def get_way(self, chara):
        x, y = chara.x, chara.y
        way = 0
        if self.get(x-1, y) != '#': way += 1
        if self.get(x+1, y) != '#': way += 1
        if self.get(x, y-1) != '#': way += 1
        if self.get(x, y+1) != '#': way += 1
        
        return way

    def is_clear(self):
        for dot in self.dots:
            if dot.exist: return False
        return True
        
    def dump(self):
        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                print self.get(x, y),
            print
        print "TIME:" + str(self.cur_time) + "/" + str(self.time) + " POINT:" + str(self.point)

class Dot:
    def __init__(self, map, x, y):
        self.map = map
        self.x = x
        self.y = y
        self.exist = True
    def update(self):
        self.map.set(self.x, self.y, '.')

