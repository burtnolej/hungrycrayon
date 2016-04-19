from datetime import datetime
from collections import OrderedDict
import inspect

class M(type):

    history=[]

    logschema = OrderedDict([("objtype",20),
                                ("time",20),
                                ("name",20),
                                ("args",20),
                                ("kwargs",20),
                                ("result",20),
                                ("ref",20),
                                ("file",20),
                                ("lineno",20),
                                ("code",20),
                                ("dunno",20)])
    
    calling_frame_schema = OrderedDict([("ref",0),
                                        ("file",1),
                                        ("lineno",2),
                                        ("code",3),
                                        ("dunno",4)])
    
    @staticmethod
    def dump():
        for record in get_history:
            print record
           
    @staticmethod
    def add(**kwargs):
        record = []
        
        for key,offset in M.logschema.iteritems():
            value="#NA"
            if kwargs.has_key(key):
                value = kwargs[key]

            record.append(str(value).ljust(offset))

        M.history.append(record)
        
    def __new__(cls,name,bases,classdict):
        
        for attr,item in classdict.items():

            if callable(item) and not attr.startswith("__"):

                def newfunc1(func):

                    def newfunc(self,*args, **kwargs):

                        current_frame = inspect.currentframe()
                        
                        def caller(field):
                            return(inspect.getouterframes(current_frame)[1][M.calling_frame_schema[field]])   

                        result = func(self,*args,**kwargs)

                        M.add(time=M.now(),
                              name=func.__name__,
                              args=args,
                              kwargs=kwargs,
                              result=result,
                              objtype="func",
                              code=caller("code"))                 

                    return newfunc

                classdict[attr] = newfunc1(item)
                
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

        return type.__new__(cls,name,bases,classdict)


    @staticmethod
    def now():
        return(datetime.now().strftime("%m%d%y %H:%M:%S.%f"))
    
    
    def get_history(self):
        for event in M.history:
            print event

class Example(object):
    __metaclass__ = M
    __slots__ = ['_x','_y']

    def square(self,value):
        return value*value

def main():
    eg = Example()
    eg.setx("foobar")
    eg.setx("foobar2")
    eg.sety("barfoo1")
    eg.sety("barfoo1")
    eg.square(25)

    print Example.get_history()

def stack():
    frame = inspect.currentframe()
    print inspect.getouterframes(frame)[1]


def inner_frame():
    stack()

def outer_frame():
    inner_frame()
        
#outer_frame()
main()