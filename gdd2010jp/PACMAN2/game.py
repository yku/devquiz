#!/usr/bin/python
from map import *

m = Map()
m.generate('lv2.txt')
while 1:
    m.dump()
    if m.is_clear():
        mes = "Congraturation!"
        break
    if m.is_quit:
        mes = "Quit"
        break
    m.input()
m.stdscr.addstr(m.h+2, 0, "[History]")
m.stdscr.addstr(m.h+3, 0, m.history)
m.stdscr.addstr(m.h+5, 0, mes)
m.stdscr.getch()
m.exit()
