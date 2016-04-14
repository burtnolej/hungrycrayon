#!/usr/bin/python


def func(**kwargs):

    print kwargs.has_key('a')

    kwargs.__setitem__('a','AAAA')

    print kwargs['a']
    
    for key,value in kwargs.iteritems():
        print key,kwargs[key]

def func2(kwargs):

    print kwargs.has_key('a')

    kwargs.__setitem__('a','AAAA')

    print kwargs['a']
    
    for key,value in kwargs.iteritems():
        print key,kwargs[key]

def func3(*kwargs):

    print kwargs.has_key('a')

    kwargs.__setitem__('a','AAAA')

    print kwargs['a']
    
    for key,value in kwargs.iteritems():
        print key,kwargs[key]

class MyClass():
    def func2(self,*arg,**kwargs):
        print "arg = " + arg[0]
        print str(len(arg)) + " args"

#func(a = 'A',
#     b = 'B',
#     c = 'C')

#m = MyClass()
#m.func2('xyz')

def c(shopkeeper,sketch,client):
    print shopkeeper
    
def cheeseshop(kind, *arguments, **keywords):
    print "-- Do you have any", kind, "?"
    print "-- I'm sorry, we're all out of", kind
    #for arg in arguments:
    #    print arg
    print arguments[0],arguments[1]
    print "-" * 40
    keys = sorted(keywords.keys())
    for kw in keys:
        print kw, ":", keywords[kw]

    k = keywords
    c(**k)

class Test(object):
    def test(self,*arg,**kwargs):
        print arg,kwargs
        
        for kw in sorted(kwargs.keys()):
            setattr(self,kw,kwargs[kw])
            #print kw,kwargs[kw]
    

#cheeseshop("Limburger", "It's very runny, sir.",
#           "It's really very, VERY runny, sir.",
#           shopkeeper='Michael Palin',
#           client="John Cleese",
#           sketch="Cheese Shop Sketch")

#t = Test()
#A='a'
#B='b'
#C='c'
#t.test(A=A,B=B,C=C)

c = [7,8,9]
d = {'A':1,'B':2,'C':3}
#func2(d)
t = Test()
t.test(*c,**d)
#t.test(d)

#print **d

#print t.A,t.B,t.C
        
#exit()

#func(**d)

#func3(*d)

