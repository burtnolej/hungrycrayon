#!/usr/bin/python

class MyModifiedDict(dict):
    def __repr__(self):
        return(str(self.__class__))
        #return("xyz")

class PlainDict(dict):
    pass

mmd = MyModifiedDict({'a':1})
print mmd

pd = PlainDict({'a':1})
print pd
