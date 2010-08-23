#!/usr/bin/python

DOWN  = 1
LEFT  = 2
UP    = 4
RIGHT = 8
FRONT = 16
BACK  = 32 

def get_next_inc(dir):
    if dir == DOWN:  return  0,  1
    if dir == LEFT:  return -1,  0
    if dir == UP:    return  0, -1
    if dir == RIGHT: return  1,  0

def get_abs_dir(base, dir):
    if base == DOWN:
        if   dir == LEFT:  return RIGHT
        elif dir == RIGHT: return LEFT
        elif dir == FRONT: return DOWN
        elif dir == BACK:  return UP
    if base == UP:
        if   dir == LEFT:  return LEFT 
        elif dir == RIGHT: return RIGHT 
        elif dir == FRONT: return UP
        elif dir == BACK:  return DOWN
    if base == LEFT:
        if   dir == LEFT:  return DOWN
        elif dir == RIGHT: return UP
        elif dir == FRONT: return LEFT
        elif dir == BACK:  return RIGHT
    if base == RIGHT:
        if   dir == LEFT:  return UP 
        elif dir == RIGHT: return DOWN 
        elif dir == FRONT: return RIGHT 
        elif dir == BACK:  return LEFT

class Enemy:
    def __init__(self, c, x, y):
        self.x = x
        self.y = y
        self.c = c
        self.prev_dir = 0
    
    def get_next_pos_deadend(self, s):
        dir = s.get_movable_dir(self.x, self.y)
        self.prev_dir = dir
        return get_next_inc(dir)
    
    def get_next_pos_aisle(self, s):
        dir = s.get_movable_dir(self.x, self.y)
        if self.prev_dir == DOWN:
            dir -= UP
        elif self.prev_dir == UP:
            dir -= DOWN
        elif self.prev_dir == LEFT:
            dir -= RIGHT
        elif self.prev_dir == RIGHT:
            dir -= LEFT
        self.prev_dir = dir
        return get_next_inc(dir)
    
    def get_pos(self):
        return self.x, self.y
    
    def move(self, x, y):
        self.x = x
        self.y = y
    def get_init_next_pos(self, s):
        dir = s.get_movable_dir(self.x, self.y)
        if dir & DOWN: 
            self.prev_dir = DOWN
            return get_next_inc(DOWN)
        if dir & LEFT:
            self.prev_dir = LEFT
            return get_next_inc(LEFT)
        if dir & UP:
            self.prev_dir = UP
            return get_next_inc(UP)
        if dir & RIGHT:
            self.prev_dir = RIGHT
            return get_next_inc(RIGHT)

class V(Enemy):
    def get_next_pos(self, s):
        next_x, next_y = 0, 0
        pacman = s.get_pacman()
        dx, dy = pacman.x - self.x, pacman.y - self.y 
        dir = s.get_movable_dir(self.x, self.y)

        if dy != 0:
            inc = 1 if dy > 0 else -1
            f = s.get_field(self.x, self.y + inc)
            if f != '#':
                next_y = inc
                self.prev_dir = DOWN if dy > 0 else UP
                return next_x, next_y
        
        if dx != 0:
            inc = 1 if dx > 0 else -1
            f = s.get_field(self.x + inc, self.y)
            if f != '#':
                next_x = inc
                self.prev_dir = RIGHT if dx > 0 else LEFT
                return next_x, next_y
        
        if dir & DOWN:
            self.prev_dir = DOWN
            return get_next_inc(DOWN)
        if dir & LEFT:
            self.prev_dir = LEFT
            return get_next_inc(LEFT)
        if dir & UP:
            self.prev_dir = UP
            return get_next_inc(UP)
        if dir & RIGHT:
            self.prev_dir = RIGHT
            return get_next_inc(RIGHT)
        
class H(Enemy):
    def get_next_pos(self, s):
        next_x, next_y = 0, 0
        pacman = s.get_pacman()
        dx, dy = pacman.x - self.x, pacman.y - self.y 
        dir = s.get_movable_dir(self.x, self.y)
         
        if dx != 0:
            inc = 1 if dx > 0 else -1
            f = s.get_field(self.x + inc, self.y)
            if f != '#':
                next_x = inc
                self.prev_dir = RIGHT if dx > 0 else LEFT
                return next_x, next_y
 
        if dy != 0:
            inc = 1 if dy > 0 else -1
            f = s.get_field(self.x, self.y + inc)
            if f != '#':
                next_y = inc
                self.prev_dir = DOWN if dy > 0 else UP
                return next_x, next_y
        
        if dir & DOWN: 
            self.prev_dir = DOWN
            return get_next_inc(DOWN)
        if dir & LEFT:
            self.prev_dir = LEFT
            return get_next_inc(LEFT)
        if dir & UP:
            self.prev_dir = UP
            return get_next_inc(UP)
        if dir & RIGHT:
            self.prev_dir = RIGHT
            return get_next_inc(RIGHT)
 
class L(Enemy):
    def get_next_pos(self, s):
        dir = s.get_movable_dir(self.x, self.y) 
        abs_dir = get_abs_dir(self.prev_dir, LEFT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, FRONT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, RIGHT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)

class R(Enemy):
    def get_next_pos(self, s):
        dir = s.get_movable_dir(self.x, self.y) 
        abs_dir = get_abs_dir(self.prev_dir, RIGHT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, FRONT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, LEFT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)

MODE_NONE = 0
MODE_L = 1
MODE_R = 2

class J(Enemy):
    mode = MODE_NONE
    def get_next_pos(self, s):
        attr = s.get_mass_attr(self.x, self.y)
        if attr >= 3: # cross
            if self.mode == MODE_L: self.mode = MODE_R
            elif self.mode == MODE_R or self.mode == MODE_NONE: self.mode = MODE_L
        if self.mode == MODE_L:
            return self.get_next_pos_L(s)
        elif self.mode == MODE_R:
            return self.get_next_pos_R(s)

    def get_next_pos_R(self, s):
        dir = s.get_movable_dir(self.x, self.y) 
        abs_dir = get_abs_dir(self.prev_dir, RIGHT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, FRONT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, LEFT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
    def get_next_pos_L(self, s):
        dir = s.get_movable_dir(self.x, self.y) 
        abs_dir = get_abs_dir(self.prev_dir, LEFT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, FRONT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)
        
        abs_dir = get_abs_dir(self.prev_dir, RIGHT)
        if dir & abs_dir:
            self.prev_dir = abs_dir
            return get_next_inc(abs_dir)



