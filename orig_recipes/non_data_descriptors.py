#!/usr/bin/python

import sys

'''
functions have a __get__() method so that they can be converted to a
method when accessed as attributes.
'''


# descriptors

class RevealAccess(object):
    '''
    data descriptor triggers function calls upon access to an attribute
    '''
    def __init__(self,initval=None,name='var'):
        self.val = initval
        self.name = name

    def __get__(self,obj,objtype):
    #def __get__(self):
        #print self
        #print obj
        obj=None
        objtype=None
        print 'retrieving',self.name,
        return self.val

    def __set__(self,obj,val):
        print 'updating', self.name
        self.val = val


class MyClass(object):
    x = RevealAccess(10,'var "x"')
    y = 5

#m = MyClass()
#print m.x
#m.x=20
#print m.x
#print m.y


class G(object):
    def h(klass,x):
        return klass.__name__,x
    h = classmethod(h)


class E(object):
    @staticmethod
    def f(x):
        print x
        pass
  
    #f = staticmethod(f)

#print G.h(3)
#print G().h(3)

#print E.f(3)
#e = E()
#print e.f(3)


class MyClass(object):
    def __init__(self):
        self.myvar = "class var"
    
    #@staticmethod
    def myfunc(oself,klass=None):
        pass

    @staticmethod
    def printargs(arg1,arg2):
        print arg1,arg2
        
    @staticmethod
    def mystaticfunc(arg,klass):
        MyClass.printargs(arg,klass.myvar)

    def myclassmethod(self,arg):
        MyClass.printargs(arg,self.myvar)

#mc = MyClass()
#mc.myclassmethod("instance method")


class MyOtherClass(object):
    def __init__(self):
        self.myvar = "static var"

moc = MyOtherClass()
#MyClass.mystaticfunc("static method",moc)


class MyFunction(object):
    def __init__(self,val=None):
        print "setting val",val
        self.myrealfunc = val
        pass
    
    def __get__(self,obj,objtype,klass=None):
        if obj:
            print
            print "being called as an instance method"
            print "of obj",obj 
            print "via descriptor",self
            print "running",
            return(self.myrealfunc(obj))
            
        else:
            print
            print "being called as a static method"
            print "of class",objtype
            print "via descriptor",self
            print klass
            return(self.myrealfunc(klass))

    def __call__(self,*args):
        print "call",args

    #def __set__(self,obj,val):
    #    print "updating"
    #    self.val = val


class MyClass(object):
    def __init__(self):
        self.myvar = "instance var"

    def myrealfunc(self):
        print self.myvar

    sm = staticmethod(myrealfunc)
        
    #myfunc = MyFunction(myrealfunc)


mc = MyClass()
mc.myrealfunc()

#print MyClass.sm
#print MyClass.myrealfunc
#print mc.myrealfunc

MyClass.sm(moc)
