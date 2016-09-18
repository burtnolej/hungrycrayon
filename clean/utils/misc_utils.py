from random import randint
import sys
from collections import OrderedDict
import sys
from types import *
from inspect import stack
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")


def thisfuncname(cls=None):
    
    funcname = stack()[1][3]
    
    if cls <> None:
        clsname = cls.__class__.__name__
        funcname = clsname + "." + funcname
    
    return(funcname)

def nxnarraycreate(maxrows,maxcols,args={}):
    ''' creates a n x n array containing args; args can be none, args can be dict, list, string'''
    grid=[]
    for row in range(maxrows):
        row=[]
        for col in range(maxcols):
            # if its a dict make a copy
            try:
                argcopy = args.copy()
            except AttributeError:
                argcopy = args
                
            row.append(argcopy)
        grid.append(row)
    return(grid)

class Singleton(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):
        
        if kwargs.has_key('reset') == True:
            cls._instances = {}
            kwargs.pop('reset')
                
        if cls not in cls._instances:
            #print "info: singleton object being created"
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)
        else:
            #print "info: singleton already instantiated",cls._instances[cls]
            pass
        return cls._instances[cls]
    
def attr_get_keyval(obj):
    from inspect import getmembers
    return[(k,v) for k,v in getmembers(obj) if not k.startswith('__')]

def os_file_exists(os_file_name):
    from os.path import exists
    
    if exists(os_file_name):
        return(True)
    else:
        return(False)

def os_file_get_wildcard(dir,pattern):
    import os, re
    return([f for f in os.listdir(dir) if re.search(pattern, f)])
       
    #os.remove(os.path.join(dir, f))

def os_file_to_string(filename,remove=None):
    
    s=""
    fh = open(filename, 'r+')

    for line in fh:
        if remove <> None:
            for _str in remove:
                line = line.replace(_str,"")
        s+=line
       
    fh.close()
    return s

def os_file_to_list(filename,remove=None):
    
    fh = open(filename, 'r+')

    l = [line for line in fh]       
    fh.close()
    return l

def write_pickle(object,filename=None):
    import pickle
    with open(filename, 'w') as f:
        pickle.dump(object, f)

    return(filename)

def read_pickle(filename):
    import pickle
    with open(filename, 'r') as f:
        object = pickle.load(f)

    return(object)

class IDGenerator(object):
    __metaclass__ = Singleton

    idfile = ".id.dat"
    usedids = []
    size = 8
        
    def __init__(self):
        from os import path as ospath
        if ospath.exists(self.idfile) == True:
            self.usedids = read_pickle(self.idfile)
        
    def getid(self):        
        from os import path as ospath

        return(self._next())
            
    def num_ids(self):
        return(len(self.usedids))

    def reset(self):
        import os
        self.usedids = []

        try:
            os.remove(self.idfile)
        except OSError:
            pass
        
    def _next(self):
        count = 1
        
        maxid = pow(10,self.size)
        unique=False
        retry=0
        
        while unique==False:
            uniqueid = randint(1,maxid)
            uniqueid = hex(uniqueid).upper()[2:].rjust(self.size,"0")
            
            if not uniqueid in self.usedids: 
                unique=True
            else:
                retry+=1
                
            if retry>10: 
                self.write()
                raise Exception("max retry")
            count += 1
        self.usedids.append(uniqueid)
        #print "adding",uniqueid
        #self.write()
        return(uniqueid)
        
    def write(self):
        write_pickle(self.usedids,self.idfile)
    
    def __del__(self):
        self.write()