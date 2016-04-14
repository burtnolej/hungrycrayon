from datetime import datetime
from collections import OrderedDict

class M(type):

    history=[]

    schema = OrderedDict(("objtype",20),
                         ("time",20),
                         ("name",20),
                         ("args",20),
                         ("kwargs",20),
                         ("result",20))
    
    @staticmethod
    def dump():
        for record in get_history:
            print record

    def add(**kwargs):
        record = []
        for key,value in M.schema:
            record.append(key.ljust(kwargs[key]))

        M.history.append(record)
        
    def __new__(cls,name,bases,classdict):
        
        for attr in classdict.get('__slots__',()):

            if attr.startswith('_'):

                def getter(self,attr=attr):

                    result=getattr(self,attr),

                    M.add(time=M.now(),
                          name=attr,
                          result=result,
                          objtype="getter")

                    return(result)

                def setter(self,value,attr=attr):

                    setattr(self,attr,value)

                    M.add(time=M.now(),
                          name=attr,
                          args=value,
                          objtype='setter')

                classdict['get' + attr[1:]] = getter
                classdict['set' + attr[1:]] = setter


        for attr,item in classdict.items():

            if callable(item) and not attr.startswith("__"):

                def newfunc1(func):

                    def newfunc(self,*args, **kwargs):

                        result = func(self,*args,**kwargs)

                        M.add(time=M.now(),
                              name=func.__name__,
                              args=args,
                              kwargs=kwargs,
                              result=result)

                    return newfunc

                classdict[attr] = newfunc1(item)

        return type.__new__(cls,name,bases,classdict)


    @staticmethod
    def now():
        return(datetime.now().strftime("%m%d%y %H:%M:%S.%f"))

class Example(object):
    __metaclass__ = M
    __slots__ = ['_x','_y']

    def square(self,value):
        return value*value

eg = Example()
eg.setx("foobar")
eg.setx("foobar2")
eg.sety("barfoo1")
eg.sety("barfoo1")
eg.square(25)

print Example.get_history
print Example.set_history
print Example.method_history

