import sys

import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils_generic import GenericBase

import unittest
import time

class ObjFactory(GenericBase):
    
    store = {}
    
    def __init__(self,reset=False):
        if reset==True:
            self.reset()
            
        super(ObjFactory,self).__init__()
    
    def new(self,clsname,**kwargs):

        for key,value in kwargs.iteritems():
            setattr(self,key,value)
        
        if hasattr(self,'objid') == False:
            raise Exception('arg objid must be set')
        
        # modname is set if the cls definitions are not in this module
        if self.modname == None:
            self.modname = __name__
            
        kwargs.pop('modname')
        
        # has a dynamic constructor been specified
        constructor=None
        if hasattr(self,'constructor'):
            constructor= kwargs.pop('constructor')
            
        # if this is the first request for this cls then create a new dict
        if self.store.has_key(clsname) == False:
            self.store[clsname] = {}
        
        # if this is the first instance of this obj then else return existing    
        if  self.store[clsname].has_key(kwargs['objid']) == False:
            # dynamically create the new object
            clsobj = getattr(sys.modules[self.modname],clsname)
            
            if constructor <> None:
                constobj = getattr(clsobj,constructor)
                newobj =constobj(**kwargs)
            else:
                newobj =clsobj(**kwargs)
            
            #newobj = getattr(sys.modules[self.modname],clsname)(objid,**kwargs)
            self.store[clsname][kwargs['objid']] = newobj
            self.log.log(3,"added obj="+newobj.__class__.__name__+" tag="+str(newobj)+" id="+newobj.id)

        return(self.store[clsname][kwargs['objid']])
        
    def query(self,clsname=None):
        if clsname == None:
            return self.store.keys()
        else:
            return [obj for name, obj in self.store[clsname].iteritems()]
    
    def object_exists(self,clsname,objid):
        return(self.store[clsname].has_key(objid))
    
    def object_get(self,clsname,objid):
        return(self.store[clsname][objid])
        
    def object_iter(self):
        for cls in self.store.values():
            for obj in cls.values():
                yield obj
                
    def reset(self):
        self.store = {}
        
    def __repr__(self):
        return('ObjFactory')
    