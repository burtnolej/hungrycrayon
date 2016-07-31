from random import randint

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

def get_obj_members(obj):
    from inspect import getmembers
    return([(_attr,_val,callable(getattr(obj,_attr))) for _attr,_val in getmembers(obj) if not _attr.startswith("__")])

def get_obj_attr_names(obj):
    return [_name for _name,_,_ in get_obj_members(obj)]

def get_obj_attr_vals(obj,notcallable=True):
    return [val for _,val,callable in get_obj_members(obj) if callable == False]
        
def get_obj_attr(obj,notcallable=True,notinternal=True):
    return [(_name,_val) for _name,_val,callable in get_obj_members(obj) 
            if callable <> notcallable and _name.startswith('__') <> notinternal]         

class generic:
    
    def __init__(self,**args):
        for key,value in args.iteritems():
            setattr(self,key,value)
            
    def __print_attr__(self):
        for attrname,attrval in self.get_attr():
            print attrname,attrval
        
    def __get_attr__(self,obj=None):
        if obj==None:
            return get_obj_attr(self)
        return(get_obj_attr(obj))
    
    def __get_attr_names__(self,obj=None):
        if obj==None:
            return get_obj_attr_names(self)
        return(get_obj_attr_names(obj))
    
    def __dump__(self):
        _setargs=[]
        from types import InstanceType
        for name,obj in self.__get_attr__(self):
            if type(obj) == InstanceType:
                _setargs.append(str(name)+"="+obj.__class__.__name__)
            else:
                _setargs.append(str(name)+"="+str(obj))
        return(_setargs)

class enum(generic):
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

class UniqueIDGenerator(object):
    #__metaclass__ = Singleton
    
    def __init__(self,filename,size):
        self.fn = filename
        self.usedids = []
        self.size=size
        
        from os import path as ospath
        
        if ospath.exists(self.fn) == True:
            #print "recovered file",self.fn
            self.usedids = read_pickle(self.fn)
            self.old_num_ids = len(self.usedids)
        else:
            self.old_num_ids = 0
            #print "initializing new",self.fn

    def num_ids(self):
        return(len(self.usedids))
        
    def next(self):
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
                #print "conflict",uniqueid
                retry+=1
                
            if retry>10: 
                self.write()
                raise Exception("max retry")
            count += 1
        self.usedids.append(uniqueid)
        
        return(uniqueid)

    def reset(self):
        self.usedids = []
        
    def write(self):
        #print "writing to",self.fn,"[",self.old_num_ids,"/",self.num_ids(),"]"
        write_pickle(self.usedids,self.fn)
        return(self.old_num_ids,self.num_ids())
    
    
    def __del__(self):
        self.write()

'<mapversion="0.9.0"><nodeTEXT="groupby.xml"><nodeTEXT="foobar"><nodeTEXT="barfoo"><nodeTEXT="boohoo"/></node></node><nodeTEXT="foobar2"><nodeTEXT="barfoo2"><nodeTEXT="boohoo2"/></node></node></node><nodeTEXT="gbyDatabase"><nodeTEXT="foobar"/><nodeTEXT="foobar2"/></node></map>'
'<mapversion="0.9.0"><nodeTEXT="groupby.xml"><nodeTEXT="foobar"><nodeTEXT="barfoo"><nodeTEXT="boohoo"/></node></node><nodeTEXT="foobar2"><nodeTEXT="barfoo2"><nodeTEXT="boohoo2"/></node></node><nodeTEXT="gbyDatabase"><nodeTEXT="foobar"/><nodeTEXT="foobar2"/></node></node></map>'
