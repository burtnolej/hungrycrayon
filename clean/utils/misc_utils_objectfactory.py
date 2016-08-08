import sys

import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils import generic

import unittest
import time

class ObjFactory(generic):
    
    store = {}
    
    def new(self,clsname,objid,**kwargs):
        
        for key,value in kwargs.iteritems():
            setattr(self,key,value)
            
        # modname is set if the cls definitions are not in this module
        if self.modname == None:
            self.modname = __name__
            
        kwargs.pop('modname')
            
        # if this is the first request for this cls then create a new dict
        if self.store.has_key(clsname) == False:
            self.store[clsname] = {}
        
        # if this is the first instance of this obj then else return existing    
        if  self.store[clsname].has_key(objid) == False:
            newobj = getattr(sys.modules[self.modname],clsname)(objid,**kwargs)
            self.store[clsname][objid] = newobj
            self.log.log(3,"added obj="+newobj.__class__.__name__+" tag="+str(newobj)+" id="+newobj.id)

        return(self.store[clsname][objid])
        
    def query(self,clsname):
        return [obj for name, obj in self.store[clsname].iteritems()]
        
    def __repr__(self):
        return('ObjFactory')
    