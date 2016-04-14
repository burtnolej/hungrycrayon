#!/usr/bin/python

from inspect import getmembers

class MyClass(object):
    def __init__(self,multiplier):
        self.multiplier = multiplier
        
    def method1(self,num):
        print "method1", str(num*self.multiplier)

    def method2(self,num):
        print "method2", str(num*self.multiplier)

    def method3(self,num):
        print "method3", str(num*self.multiplier)

class MyCompClass(object):
    def __init__(self,multiplier):
        self.other = MyClass(multiplier)
        
    def method1(self,num):
        self.other.method1(num)
        
mc = MyClass(10)
mc.method1(4)
mc.method2(5)

mcc = MyCompClass(10)
mcc.method1(4)
mcc.method2(5)




