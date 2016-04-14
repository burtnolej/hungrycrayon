#!/usr/bin/python


from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import file2list

cpy = file2list("./cpy.dat")


s = "TRAVE"

if s in (el[0:len(s)] for el in cpy):
    print "found " + s

r = [el for el in cpy if el[0:len(s)] == s]
print r
