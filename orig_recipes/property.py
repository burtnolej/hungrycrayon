#!/usr/bin/python


class MyClass(object):
    @property
    def x(self):
        return "xyz"

    @x.setter
    def x(self,value):
        pass

myclass = MyClass()
print myclass.x

myclass.x = 123
print myclass.x


