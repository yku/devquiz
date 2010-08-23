#!/usr/bin/python

from stage import *
import curses
import copy

s = Stage('lv2.txt')

scr = curses.initscr()
curses.start_color()
curses.noecho()
scr.keypad(1)
curses.cbreak()

curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

history = ""
while 1:
    # draw map
    scr.clear()
    for y in xrange(0, s.h):
        for x in xrange(0, s.w):
            scr.addstr(y, x, s.get_field(x, y))
    # draw pacman
    pacman = s.get_pacman()
    scr.addstr(pacman.y, pacman.x, pacman.c, curses.color_pair(2))
    # draw enemies
    es = s.get_enemies()
    for e in es:
        scr.addstr(e.y, e.x, e.c, curses.color_pair(3))
    scr.addstr(y+1, 0, "TIME:" + str(s.cur_time) + "/" + str(s.time) + " POINT:" + str(s.point))
   
    # CPU turn
    copy_s = copy.copy(s)
    for e in es:
        if s.cur_time == 0:
            dx, dy = e.get_init_next_pos(copy_s)
        else:
            mass = copy_s.get_mass_attr(e.x, e.y)
            if mass == 1: # dead end
                dx, dy = e.get_next_pos_deadend(copy_s)
            elif mass == 2: # aisle
                dx, dy = e.get_next_pos_aisle(copy_s)
            else:
                dx, dy = e.get_next_pos(copy_s)
        s.update(e, dx, dy)

    # input
    key = scr.getch()
    scr.refresh()
    if key == ord('h'):
        history += "h"
        s.update(pacman,-1,0) 
    elif key == ord('j'):
        history += "j"
        s.update(pacman,0,1) 
    elif key == ord('k'):
        history += "k"
        s.update(pacman,0,-1) 
    elif key == ord('l'):
        history += "l"
        s.update(pacman,1,0) 
    elif key == ord('q'):
        break
    else:
        history += "."
        s.update(pacman,0,0)

scr.addstr(y+2, 0, history)
scr.getch()
curses.nocbreak()
scr.keypad(0)
curses.echo()
curses.endwin()
