#!/usr/bin/python
import inspect
import copy
from sys import path,argv,exit,stdout
from datetime_util import MyDT

class LogMeta(type):
    call_stack=[]
    count=0
    store=[]

    @staticmethod
    def add(func_name):
        LogMeta.count+=1 
        LogMeta.call_stack.append(func_name)

    @staticmethod
    def remove(func_name):
        LogMeta.call_stack.remove(func_name)
        LogMeta.count-=1
        
    @staticmethod
    def format_clsnm(*arg):
        a_str=""
        for a in arg:
            if hasattr(a,'__name__'):
                a_str += str(a.__name__)
            else:
                a_str = str(arg)
        return(a_str)

    @staticmethod
    def pprint(lh=None):
        if not lh:
            import sys
            lh = sys.stdout   
        
        for logitem in LogMeta.store:
            print logitem['time'],
            print logitem['class'],
            print logitem['super'],
            print logitem['function'],
            print logitem['len'],
            print logitem['class'],
            print logitem['args'],
            print logitem['results']
            
        
    @staticmethod
    def output(cls,func_name,res,*arg,**kw):
        offset=15
        _output = {}
        
        _stack = copy.deepcopy(LogMeta.call_stack)
        _stack.reverse() # keeps calls in order executes
        _output['time'] = int(MyDT.now(display_fmt='%f').value)
        _output['class'] = type(cls).__name__
        _output['super'] = type(cls).__bases__[0].__name__
        _output['function'] = ((len(_stack)-1) * " ") + func_name
        _output['len'] = len(_stack)
        _output['args'] = arg
        _output['results'] = res

        return(_output)

    def orig____new__(cls,name,bases,classdict):
        for attr, item in classdict.items():
            if callable(item) and not attr.startswith("__"):
                    def newfunc1(func):
                        def newfunc(self,*arg,**kwargs):
                            
                            LogMeta.add(func.__name__)
                            if hasattr(func,'log'): #
                                res = func(self,*arg,**kwargs)
                                cls.store.append(cls.output(self,func.__name__,res,arg,kwargs))
                                
                            else:
                                res = func(self,*arg,**kwargs)
                            LogMeta.remove(func.__name__)
                            return res
                        return newfunc
                    classdict[attr] = newfunc1(item)
        return type.__new__(cls,name,bases,classdict)

    def __new__(cls,name,bases,classdict):
        for attr, item in classdict.items():
            if callable(item) and not attr.startswith("__"):
                    def newfunc1(func):
                        def newfunc(self,*arg,**kwargs):
                            
                            LogMeta.add(func.__name__)

                            res = func(self,*arg,**kwargs)
                            print cls.output(self,func.__name__,res,arg,kwargs)

                            LogMeta.remove(func.__name__)
                            return res
                        return newfunc
                    classdict[attr] = newfunc1(item)
        return type.__new__(cls,name,bases,classdict)