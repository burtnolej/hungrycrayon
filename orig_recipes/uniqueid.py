#!/usr/bin/python

from random import randint
from sys import path,argv,exit
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import write_object_to_disk,read_object_from_disk,Singleton
from os import path as ospath


class UniqueIDGenerator(object):
    __metaclass__ = Singleton
    
    def __init__(self,id_len=7):
        self.fn = "./uniqueid.dat"
        self.id_len = id_len
        self.list = []
        self.uniqueid = None

        if ospath.isfile(self.fn):
            self.list = read_object_from_disk(self.fn)

    def stats(self):
        return(len(self.list))
        
    def next(self):
        count = 1
        self.uniqueid = str(randint(1,9999999)).ljust(7,'0')
        while (self.uniqueid in self.list):
            self.uniqueid = str(randint(1,9999999)).ljust(7,'0')
            count += 1
        self.list.append(self.uniqueid)
        
        #return(str(len(self.list)),self.uniqueid,str(count))
        return(self.uniqueid)

    def reset(self):
        self.list = []
        self.uniqueid = None
        
    def __del__(self):
        write_object_to_disk(self.list,self.fn)

    
if __name__ == '__main__':

    uniqueidgen = UniqueIDGenerator()
    if len(argv) > 1:
        if argv[1] == "reset":
            uniqueidgen.reset()
        elif argv[1] == "query":
            print "number of ids issues: " + str(uniqueidgen.stats())
    else:
            print "usage : uniqueid.py [reset|query]"
    
    uniqueidgen.__del__()
    exit()
