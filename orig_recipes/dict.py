#!/usr/bin/python


class MyDict(dict):
    def __init__(self,key,value):
        self._myattr = "xyz"
        self[key] = value


md = MyDict("123","456")
md["123"] = "456"

for k,v in md.iteritems():
    print k,v


print dir(md)
    
