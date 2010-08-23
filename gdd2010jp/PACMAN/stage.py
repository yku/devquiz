#!/usr/bin/python
# coding: UTF-8
from pacman import *
from enemy import *

class Stage:
    def __init__(self, filename):
        f = open(filename)
        self.time = int(f.readline())
        self.cur_time = int(0)
        self.point = int(0)
        self.enemies = []
        w, h = f.readline().split(' ')
        self.w = int(w)
        self.h = int(h)
        self.stage = [0 for i in xrange(self.w * self.h)]
        x, y = 0, 0
        for c in f.read():
            if c == '\n':
                x = 0
                y += 1
                continue
            if c == '@':
                self.pacman = Pacman(x, y)
                t = ' '
            elif c == 'V':
                self.enemies.append(V(c, x, y))
                t = ' '
            elif c == 'H':
                self.enemies.append(H(c, x, y))
                t = ' '
            elif c == 'L':
                self.enemies.append(L(c, x, y))
                t = ' '
            elif c == 'R':
                self.enemies.append(R(c, x, y))
                t = ' '
            elif c == 'J':
                self.enemies.append(J(c, x, y))
                t = ' '
            elif c == '.': t = c
            elif c == ' ': t = c
            elif c == '#': t = c

            self.stage[y * self.w + x] = t
            x += 1
    
    def update(self, obj, dx, dy):
        x, y = obj.get_pos()
        next_obj = self.get_field(x+dx, y+dy)
        obj.move(x+dx, y+dy)
        if isinstance(obj, Pacman):
            if next_obj == '.': self.point += 1
            self.set_field(x+dx, y+dy, ' ') 
            self.cur_time += 1
        if self.cur_time > self.time:
            print "GAME OVER"
            exit()

    def get_pacman(self):
        return self.pacman
    def get_enemies(self):
        return self.enemies

    def get_field(self, x, y):
        return self.stage[y * self.w + x]
    def set_field(self, x, y, val):
        self.stage[y * self.w + x] = val
    
    def get_mass_attr(self, x, y):
        dir = self.get_movable_dir(x, y)
        bit = 0
        while dir:
            if dir & 1:
                bit += 1
            dir = dir >> 1
        return bit

    def get_movable_dir(self, x, y):
        dir = 0
        left  = self.get_field(x-1, y)
        up    = self.get_field(x, y-1)
        right = self.get_field(x+1, y)
        down  = self.get_field(x, y+1)
        if left  != '#': dir += LEFT      
        if up    != '#': dir += UP
        if right != '#': dir += RIGHT  
        if down  != '#': dir += DOWN
        return dir 
