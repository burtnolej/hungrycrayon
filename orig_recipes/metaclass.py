#!/usr/bin/python
import inspect
import copy

def metaclass_basic():
    class M(type):
        times=0
        def __new__(cls,name,bases,classdict):
            print "cls",cls
            print "name",name
            print "bases",bases
            print "classdict",classdict
        
            for attr in classdict.get('__slots__',()):
                if attr.startswith('_'):
                    def getter(self,attr=attr):
                        print "getting"+attr+" + "+getattr(self,attr)
                        M.times+=1
                        return(getattr(self,attr))
                    def setter(self,value,attr=attr):
                        print "setting"+attr+" to "+value
                        setattr(self,attr,value)
                        M.times+=1
                    classdict['get' + attr[1:]] = getter
                    classdict['set' + attr[1:]] = setter
            return type.__new__(cls,name,bases,classdict)
           
    class Point(object):
        __metaclass__ = M
        __slots__=['_x','_y']


        #point = Point()
        #point.setx("XXX")
        point = Point()
        point.setx("XXX")
        point = Point()
        point.setx("XXX")
        point = Point()
        point.setx("XXX")
        point = Point()
        point.setx("XXX")
        print point.getx()
        print dir(Point)
        print Point.times
     

def metaclass_for_logging():
    class LogMeta(type):
        call_stack=[]
        count=0

        @staticmethod
        def add(func_name):
            LogMeta.count+=1 
            LogMeta.call_stack.append(func_name)

        @staticmethod
        def remove(func_name):
            LogMeta.call_stack.remove(func_name)
            LogMeta.count-=1

        @staticmethod
        def gen_str(func_name,arg):
            _stack = copy.deepcopy(LogMeta.call_stack)
            _stack.reverse() # keeps calls in order executes
            prn_str  = "->"
            prn_str += func_name + ","
            prn_str += str(arg) + ","
            prn_str += str(_stack[1:]) + "," # remove self
            prn_str += str(len(_stack))
            return(prn_str)

        @staticmethod
        def prn_str(func_name,arg):
            if not arg: # out of function
                prn_str  = "<-"
                prn_str += func_name
                print prn_str
            else: # going into function
                text = LogMeta.gen_str(func_name,arg)
                print text.ljust(5*LogMeta.count)

        def __new__(cls,name,bases,classdict):
            for attr, item in classdict.items():
                if callable(item) and not attr.startswith("__"):
                        def newfunc1(func):
                            def newfunc(self,*arg,**kwargs):
                                LogMeta.add(func.__name__)
                                if hasattr(func,'log'): #
                                    LogMeta.prn_str(func.__name__,*arg,**kwargs)
                                    func(self,*arg,**kwargs)
                                    LogMeta.prn_str(func.__name__)
                                else:
                                    func(self,*arg,**kwargs)
                                LogMeta.remove(func.__name__)
                            return newfunc
                        classdict[attr] = newfunc1(item)
            return type.__new__(cls,name,bases,classdict)

    class ClassLogMeta():
        __metaclass__ = LogMeta

        def funcA(self,*arg):
            self.funcB("C")

        def funcB(self,*arg):
            self.funcC(*arg)
            
        def funcC(self,*arg):
            pass
        
        funcC.log = True
        funcA.log = True

    clm = ClassLogMeta()
    clm.funcA("A")
    #clm.funcB("B")
    

metaclass_for_logging()
