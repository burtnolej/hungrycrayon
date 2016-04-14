#!/usr/bin/python

class A():
    def __init__(self):
        print "a"

class B(A):
    def __init__(self):
        print A.__init__(self)
        #print super(B,self)
        #super(B,self).__init__()
        print "b"

c = B()
