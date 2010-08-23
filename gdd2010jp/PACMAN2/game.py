#!/usr/bin/python
from map import *

m = Map()
m.generate('lv1.txt')
m.dump()
while 1:
    m.input()
    m.cur_time += 1
    m.dump()
    if m.is_clear(): break
print "Congraturation!"
