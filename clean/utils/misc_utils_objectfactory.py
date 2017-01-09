import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
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
from inspect import getmembers
    
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
                if hasattr(getattr(obj,k),'name'):
                    if getattr(obj,k).name <> v:
                        match=False
                else:
                    if getattr(obj,k) <> v:
                        match=False
                    
            if match==True:
                results.append(obj)
                
        return(results)
    
    def object_exists(self,clsname,objid):
        return(self.store[clsname].has_key(objid))
    
    def object_get(self,clsname,objid):
        return(self.store[clsname][objid])
    
    def object_get_byval(self,clsname,value):
        for name, obj in self.store[clsname].iteritems():
            if name == value:
                return obj
        return None
        
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

    def dumpobjrpt(self,fields=None,objtypes=None,objref=True, 
                   omitfields=[],fieldnames=False,constraints=None,fieldhdr=False):
        ''' provides more control over the output of dumpobj '''
        
        ''' set objref to false if want to exclude the python internal ref (if your testing etc)
            testing for name attributes as sometime object does not have __repr__ setup (like lesson)
        
            sample results:
            ['1038f2190', 'ROOT', 'adult', u'Amelia'], 
            ['1038f2250', 'ROOT', 'student', u'Clayton'], 
            ['1038f2310', 'ROOT', 'id', u'054C4D26'], 
            ['1038f2190', u'1.2.2.6.22', 'adult', u'Amelia'], 
            ['1038e8f10', u'1.2.2.6.22', 'dow', u'TU'], 
            ['1038f2310', u'1.2.2.6.22', 'id', u'054C4D26'],
            ['1038f23d0', u'1.2.2.6.22', 'objtype', 'lesson'], 
            ['1038e8e50', u'1.2.2.6.22', 'period', u'830-910'], 
            
            use something like below to pretty print:
            
            output.sort() # to line up the same objects
            for _output in output:
                _o_str = ""  
                for _o in _output:
                    _o_str+=str(_o).ljust(12)[:12]
            
                print _o_str
        '''
        
        '''objtypes=['lesson','subject']
        fields=['adult','student']'''
        
        allfields=False
        
        if constraints == None:
            constraints={}
            
        if fields == None:
            fields = ['objtype']
        elif fields == ['all']:
            allfields=True
        else:
            fields.append('objtype')
            
        output = []
        
        if fieldhdr == True:
            pass
            
        for record in self.dumpobj(objtypes):
      
            _output=[]
            constraint_hit=False
            
            if objref==True:            
                _output.append(record['obj'].__str__().split("0x")[1][:-1])
            
            _output.append(record['pobjid'])
            
            if allfields == True:
                fields=[]
                for attr,val in getmembers(record['obj']):
                    if callable(val) == False and attr.startswith("__") == False and attr.startswith("tbl_") == False and attr <> "database":
                        fields.append(attr)
            
            for field in fields:
                _ostr = ""
                if field in omitfields:
                    continue
                if hasattr(record['obj'],field):
                    if hasattr(getattr(record['obj'],field),'name'):
                        attrval = getattr(record['obj'],field).name
                    else:
                        attrval = getattr(record['obj'],field)
                    
                    if isinstance(attrval,dict):
                        for k,v in attrval.iteritems():
                            _ostr = k+"="+str(v)
                            if fieldnames == True:
                                _ostr = field + ":" + _ostr
                            _output.append(_ostr)
                            
                    elif constraints.has_key(field) and not attrval in constraints[field]:
                            constraint_hit=True
                    else:
                        _ostr = str(attrval)
    
                elif record.has_key(field):
                    _ostr = record[field]
                else:
                    _ostr = "-"
                    
                if fieldnames == True:
                    _output.append(field + ":" + _ostr)
                else:
                    _output.append(_ostr)      
                
            
            
            if constraint_hit == False:
                output.append(_output)
        return output
            
    def dumpobj(self,objtypes=None):
        
        suppress_objects=True
        maxdepth=2
        
        def _dumpobj(results,depth,objtypes,**kw):
            depth+=1
            result=kw
            for k,v in kw['obj'].attr_get_keyval(False):
                if type(v) not in [IntType,StringType,UnicodeType] and depth <= maxdepth:
                    
                    if hasattr(v,'objid'): # make sure its actual data not ref data like a database
                        
                        if objtypes <> None and v.__class__.__name__ not in objtypes:
                            continue
                        _dumpobj(results,depth,objtypes,
                                 obj=v,
                                 objtype=v.__class__.__name__,
                                 objid=v.objid,
                                 pobjid=kw['objid'])
                result[k]=v
            results.append(result)
        
        results = []
        depth=0

        if objtypes == None:
            objtypes = self.store.keys()
        
        for objtype in objtypes:
            for objid in self.store[objtype]:
                obj = self.store[objtype][objid]
                _dumpobj(results,depth,objtypes,
                         obj=obj,
                         objtype=objtype,
                         objid=objid,
                         pobjid="ROOT")
                
        return results
            
    def __repr__(self):
        return('ObjFactory')
    


    
