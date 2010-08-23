#!/usr/bin/python
from map import *

m = Map()
m.generate('lv1.txt')
while 1:
    m.dump()
    m.input()
    m.cur_time += 1
