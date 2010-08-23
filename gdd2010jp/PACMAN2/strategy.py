#!/usr/bin/python
from defines import *

def first(e):
    m = e.map
    if   m.is_dir(e, DOWN):
        e.down()
        return True
    elif m.is_dir(e, LEFT):
        e.left()
        return True
    elif m.is_dir(e, UP): 
        e.up()
        return True
    elif m.is_dir(e, RIGHT):
        e.right()
        return True
    return False

def one_way(e):
    return first(e)

def two_way(e):
    m = e.map
    if   m.is_dir(e, DOWN)  and e.dir != UP:
        e.down()
        return True
    elif m.is_dir(e, LEFT)  and e.dir != RIGHT:
        e.left()
        return True
    elif m.is_dir(e, UP)    and e.dir != DOWN:
        e.up()
        return True
    elif m.is_dir(e, RIGHT) and e.dir != LEFT:
        e.right()
        return True
    return False

def dy_move(e):
    m = e.map
    p = m.pacman
    dy = p.y - e.y
    if dy > 0 and m.is_dir(e, DOWN):
        e.down()
        return True
    elif dy < 0 and m.is_dir(e, UP):
        e.up()
        return True
    return False

def dx_move(e):
    m = e.map
    p = m.pacman
    dx = p.x - e.x
    if dx > 0 and m.is_dir(e, RIGHT):
        e.right()
        return True
    elif dx < 0 and m.is_dir(e, LEFT):
        e.left()
        return True
    return False

def turn_left_and_go(e):
    dir = e.dir
    m = e.map
    if dir == DOWN:
        if m.is_dir(e, RIGHT):
            e.right()
            return True
    elif dir == LEFT:
        if m.is_dir(e, DOWN):
            e.down()
            return True
    elif dir == UP:
        if m.is_dir(e, LEFT):
            e.left()
            return True
    elif dir == RIGHT:
        if m.is_dir(e, UP):
            e.up()
            return True
    return False

def go_straight(e):
    dir = e.dir
    m = e.map
    if dir == DOWN:
        if m.is_dir(e, DOWN):
            e.down()
            return True
    elif dir == LEFT:
        if m.is_dir(e, LEFT):
            e.left()
            return True
    elif dir == UP:
        if m.is_dir(e, UP):
            e.up()
            return True
    elif dir == RIGHT:
        if m.is_dir(e, RIGHT):
            e.right()
            return True
    return False

def turn_right_and_go(e):
    dir = e.dir
    m = e.map
    if dir == DOWN:
        if m.is_dir(e, LEFT):
            e.left()
            return True
    elif dir == LEFT:
        if m.is_dir(e, UP): 
            e.up()
            return True
    elif dir == UP:
        if m.is_dir(e, RIGHT): 
            e.right()
            return True
    elif dir == RIGHT:
        if m.is_dir(e, DOWN):
            e.down()
            return True
    return False

def v(e):
    if dy_move(e): return
    if dx_move(e): return 
    if first(e):   return 

def h(e):
    if dx_move(e): return
    if dy_move(e): return 
    if first(e):   return 

def l(e):
    if turn_left_and_go(e):  return 
    if go_straight(e):       return 
    if turn_right_and_go(e): return

def r(e):
    if turn_right_and_go(e): return
    if go_straight(e):       return 
    if turn_left_and_go(e):  return 

def j(e):
    if e.mode == 'L': l(e)
    elif e.mode == 'R': r(e)
