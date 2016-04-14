#!/usr/bin/python
import inspect

def singleton(class_):
    '''
    decorator implementation of a singleton
    con is that MyClass is not a class its a function so you cannot
    cal class methods
    '''
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args,**kwargs)
        return instances[class_]
    return getinstance

class Singleton(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)
        return cls._instances[cls]
            
             
@singleton
class MyClass(object):
    pass

class MyClass(object):
    pass
    #__metaclass__ = Singleton

a = MyClass()
b = MyClass()

if a is b:
    print True
else:
    print False
