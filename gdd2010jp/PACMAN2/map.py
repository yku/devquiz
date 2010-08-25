#!/usr/bin/python
from character import *
from defines import *
import curses

class Map:
    def __init__(self, curses_enable = True):
        self.curses_enable = curses_enable
        self.w = self.h = 0
        self.time = self.cur_time = int(0)
        self.point = int(0)
        self.enemies = []
        self.dots = []
        self.history = ""
        self.is_quit = False
        if self.curses_enable: self.init_curses()
    
    def exit(self):
        if self.curses_enable: self.exit_curses()

    def init_curses(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        self.stdscr.keypad(1)
        curses.cbreak()
        curses.init_pair(0, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED,   curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def exit_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

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
            key = self.stdscr.getkey() if self.curses_enable else raw_input()
            if   key == 'h' and self.is_dir(self.pacman, LEFT):
                self.pacman.left()
                self.pacman.history += key
                break
            elif key == 'j' and self.is_dir(self.pacman, DOWN):
                self.pacman.down()
                self.pacman.history += key
                break
            elif key == 'k' and self.is_dir(self.pacman, UP):
                self.pacman.up()
                self.pacman.history += key
                break
            elif key == 'l' and self.is_dir(self.pacman, RIGHT):
                self.pacman.right()
                self.pacman.history += key
                break
            elif key == '.':
                self.pacman.history += key
                break
            elif key == 'q':
                self.is_quit = True
                return

        for e in self.enemies:
            e.update()
        self.pacman.update()
        self.cur_time += 1

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
    
    def timeup(self):
        if self.cur_time >= self.time: return True
        return False

    def is_collision(self):
        p = self.pacman
        for e in self.enemies:
            if p.x == e.x and p.y == e.y: return True
            if self.is_swap(p, e): return True
        return False

    def is_swap(self, p, e):
        if p.prev_x == e.x and p.prev_y == e.y and p.x == e.prev_x and p.y == e.prev_y: return True
        return False
        
    def dump(self):
        if self.curses_enable: self.curses_dump()
        else:                  self.raw_dump()

    def curses_dump(self):
        self.stdscr.clear()
        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                c = self.get(x, y)
                if c == '@': self.stdscr.addstr(y, x, c, curses.color_pair(2))
                elif c.isalpha(): self.stdscr.addstr(y, x, c, curses.color_pair(3))
                else: self.stdscr.addstr(y, x, c)
        self.stdscr.addstr(self.h+1, 0, "TIME:" + str(self.cur_time) + "/" + str(self.time) + " POINT:" + str(self.point))
        self.stdscr.refresh()

    def raw_dump(self):
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

