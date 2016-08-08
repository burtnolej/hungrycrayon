from random import randint
import sys

import sys
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils_generic import GenericBase

class generic(GenericBase):
    def __init__(self,**kwargs):
        super(generic,self).__init__(**kwargs)
        
        self.log = Log()
        self.id =  IDGenerator().getid()
        
class Singleton(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            #print "info: singleton object being created"
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)
        else:
            #print "info: singleton already instantiated",cls._instances[cls]
            pass
        return cls._instances[cls]
    
class Log():    
    __metaclass__ = Singleton
    
    logpath = '/home/burtnolej/log.log'
    logfile = open(logpath,"a")
    verbosity = 5
    cache=[]
        
    def __repr__(self):
        return ('log')
    
    def log_cache_reset(self):
        self.cache=[]
        
    def log(self,obj,priority,*args):
        from inspect import stack
        from os.path import basename
        from datetime import datetime
        
        if priority < self.verbosity:
            logitem = []
            
            if priority == 3:
                logitem.append("sev=info")
            
            now = datetime.now().strftime("%H:%M:%S")
            msecs = str(int(datetime.now().microsecond/1000)).rjust(4,"0")
            
            callerframe = stack()[2]
            
            _logitem = generic(clr=str(obj),
                               t=now+"."+msecs,
                               clrf=callerframe[3],
                               clrfnln=str(callerframe[2]),   
                               msg=" ".join(list(args)),
                               clrfr="("+basename(callerframe[1])+")")
                               
                                 
            
            logitem = logitem + ["clr="   + str(obj),
                                 "t="     + now+"."+msecs,
                                 "clrfn=" + callerframe[3],
                                 "clrfnln=",str(callerframe[2]),   
                                 "msg="   + " ".join(list(args)),
                                 "clrf="  + "("+basename(callerframe[1]) + ")"]
    
            _content = [(_key+"="+str(_val)) for _key,_val in _logitem.attr_get_keyval(include_callable=False)]
            content = ";".join(_content)+"\n"
            self.logfile.write(content)
            self.cache.append(_logitem)
            
    def log_get_session_content(self):
        return(self.cache)
    
    def logexists(self):
        return(os_file_exists(self.logpath))

    def log_get_session_num_entries(self):
        return(len(self.cache))
    
    def log_file_length(self):
        for i,l in enumerate(self.logfile):
            pass
        return(i)
    
    def __del__(self):
        self.logfile.close()


    
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
            self.log(3,"added obj="+newobj.__class__.__name__+" tag="+str(newobj)+" id="+newobj.id)

        return(self.store[clsname][objid])
        
    def query(self,clsname):
        return [obj for name, obj in self.store[clsname].iteritems()]
        
    def __repr__(self):
        return('ObjFactory')
    
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

class enum(GenericBase):
    pass

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