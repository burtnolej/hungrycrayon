#!/usr/bin/python

import inspect

def log(func):
    def _logged(*args, **kw):
        print "[LD] func", func.__name__, "called with:", args, kw
        result = func(*args, **kw)
        print "[LD] func", func.__name__, "returned:", result
        return result
    return _logged

class A(object):
    def __init__(self):
        for x in inspect.getmembers(self, (inspect.ismethod)):
            if not x[0].startswith('__'):
                print log(getattr(self,x[0]))
                setattr(self, x[0], log(getattr(self, x[0])))

    def hello(self,text):
        print "Hello " + text

    def bye(self,text):
        print "Bye " + text
        return 0

## explicit decorators
def outer(func):
    def inner():
        print "before some func"
        ret = func()
        return ret+1
    return inner

@outer
def foo():
    return 1

# passing args to decorator
    
def myDecorator(myargs):
    def actualDecorator(func):
        def wrapper(*args, **kwargs):
            print myargs
            return func(*args,**kwargs)
        return wrapper
    return actualDecorator

@myDecorator("foobar")
def foobar():
    return("xyz")

# class decorators
class myclsdec(object):
    def __init__(self,func):
        self.func = func
        self.lvar = 0
    def __call__(self,*k,**kw):
        self.lvar += 1
        return f(self.lvar)

def verbose(func):
    def _verbose(*args,**kw):
        func(*args,**kw)
    return _verbose

if __name__ == '__main__':
    #a = A()
    #a.hello('HELLO')
    #a.bye('BYE')

    #decorated = outer(foo)
    #print decorated()
    #print foo()

    @verbose
    def mytest(*args):
        print args

    mytest('xyzz','sdfdf','adfadfdfsdfsdf')
    #print foobar()
