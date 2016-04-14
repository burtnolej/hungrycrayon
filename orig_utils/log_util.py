#!/usr/bin/python
import inspect
import copy
from sys import path,argv,exit,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from datetime_util import MyDT
from table_print import Table

class LogMetaTable(Table):
    ''''
    prints log stores in the form "time","super","func","stack_len",
    "args","results"]. log store is a list of dicts
    '''

    fields = ["time","super","function","len","args","results"]
    def __init__(self,*args,**kwargs):
        super(LogMetaTable,self).__init__(*args,**kwargs)
        
    def _cell_generator(self,object):
        column_titles = self.fields
        yield column_titles

        for i in object:
            yield [i[f] for f in self.fields]

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
                    
        lm_table = LogMetaTable(LogMeta.store,_max_column_width=35,_page=False)
        lm_table.printout(lh)

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

    def __new__(cls,name,bases,classdict):
        for attr, item in classdict.items():
            if callable(item) and not attr.startswith("__"):
                    def newfunc1(func):
                        def newfunc(self,*arg,**kwargs):
                            
                            LogMeta.add(func.__name__)
                            if hasattr(func,'log'): #
                                res = func(self,*arg,**kwargs)
                                #print arg
                                cls.store.append(cls.output(self,func.__name__,res,arg,kwargs))
                                
                            else:
                                res = func(self,*arg,**kwargs)
                            LogMeta.remove(func.__name__)
                            return res
                        return newfunc
                    classdict[attr] = newfunc1(item)
        return type.__new__(cls,name,bases,classdict)
