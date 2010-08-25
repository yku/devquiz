#!/usr/bin/python
from map import *

m = Map()
m.generate('lv3.txt')
while 1:
    m.dump()
    if m.is_clear():
        mes = "Congraturation!"
        break
    if m.is_quit:
        mes = "Quit"
        break
    if m.timeup():
        mes = "Time up!"
        break
    if m.is_collision():
        mes = "GAME OVER"
        break
    m.input()
m.stdscr.addstr(m.h+2, 0, mes)
m.stdscr.addstr(m.h+3, 0, "[History]")
m.stdscr.addstr(m.h+4, 0, m.pacman.history)
m.stdscr.getch()
m.exit()
