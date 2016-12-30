import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
          pidlogname=True,proclogname=False)

import os
from os import path as ospath
from misc_utils import thisfuncname
from misc_utils_generic import GenericBase
from inspect import isclass
import unittest
import time
from collections import OrderedDict
from types import StringType,IntType, UnicodeType
    
class ObjFactory(GenericBase):
    
    store = {}
    
    def __init__(self,reset=False):
        if reset==True:
            self.reset()
            
        super(ObjFactory,self).__init__()
    
    def _factory(self,name,cls):
        def __init__(self,**kwargs):
            cls.__init__(self,**kwargs)
            
        newclass = type(name, (cls,),{'__init__':__init__})
        return newclass         
                
    #@logger(log) 
    def new(self,basecls,clsname,**kwargs):
        
        cls = self._factory(clsname,basecls)

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
        #if hasattr(self,'constructor'):
        if kwargs.has_key('constructor'):
            constructor= kwargs.pop('constructor')
            
        # if this is the first request for this cls then create a new dict
        if self.store.has_key(clsname) == False:
            #self.store[clsname] = {}
            self.store[clsname] = OrderedDict()
        
        # if this is the first instance of this obj then else return existing    
        if  self.store[clsname].has_key(kwargs['objid']) == False:
            # dynamically create the new object
            #clsobj = getattr(sys.modules[self.modname],clsname)
            
            if isinstance(cls,object) == False:
                raise Exception('module',self.modname,'is returning',clsname,'as type',type(cls), \
                                'must be object. member attr may have same name as class')

            if constructor <> None:
                constobj = getattr(cls,constructor)
                newobj =constobj(**kwargs)
            else:
                newobj =cls(**kwargs)

            #newobj = getattr(sys.modules[self.modname],clsname)(objid,**kwargs)
            if newobj == "":
                log.log(thisfuncname(),2,msg="could not create an instance")
            else:
                self.store[clsname][kwargs['objid']] = newobj
                log.log(thisfuncname(),20,msg="created",newobj=newobj,kwargs=kwargs)
            
        else:
            log.log(thisfuncname,15,msg="key conflict",kwargs=kwargs)

        return(self.store[clsname][kwargs['objid']])
        
    def query(self,clsname=None):
        if clsname == None:
            return self.store.keys()
        else:
            return [obj for name, obj in self.store[clsname].iteritems()]
        
    def query_advanced(self,clsname,constraints):
        results =[]
        for name, obj in self.store[clsname].iteritems():
            match=True
            for k,v in constraints:
                #if getattr(obj,k).name <> v:
                if getattr(obj,k) <> v:
                    match=False
            if match==True:
                results.append(obj)
                
        return(results)
    
    def object_exists(self,clsname,objid):
        return(self.store[clsname].has_key(objid))
    
    def object_get(self,clsname,objid):
        return(self.store[clsname][objid])
        
    def object_iter(self):
        for cls in self.store.values():
            for obj in cls.values():
                yield obj
                
    def object_serialize(self,obj):
        items = []
        for k,v in obj.attr_get_keyval(include_callable=False,
                                       include_nondataattr=False):
            try:
                items.append("{k}={v}".format(k=k,v=v))
            except:
                items.append("{k}={v}".format(k=k,v='e'))
        return(",".join(items))
                
    def reset(self):
        self.store = {}

    def dumpobj(self):
        
        suppress_objects=True
        maxdepth=2
        
        def _dumpobj(results,depth,**kw):
            depth+=1
            result=kw
            for k,v in kw['obj'].attr_get_keyval(False):
                if type(v) not in [IntType,StringType,UnicodeType] and depth <= maxdepth:
                    
                    if hasattr(v,'objid'): # make sure its actual data not ref data like a database
                        _dumpobj(results,depth,
                                 obj=v,
                                 objtype=v.__class__.__name__,
                                 objid=v.objid,
                                 pobjid=kw['objid'])
                result[k]=v
            results.append(result)
        
        results = []
        depth=0
        for objtype in self.store.keys():
            for objid in self.store[objtype]:
                obj = self.store[objtype][objid]
                _dumpobj(results,depth,
                         obj=obj,
                         objtype=objtype,
                         objid=objid,
                         pobjid="ROOT")
                
        return results
            
    def __repr__(self):
        return('ObjFactory')
    


    
