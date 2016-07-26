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

           
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------

def get_obj_members(obj):
    from inspect import getmembers
    return([(_attr,_val,callable(getattr(obj,_attr))) for _attr,_val in getmembers(obj) if not _attr.startswith("__")])

def get_obj_attr_names(obj):
    return [_name for _name,_,_ in get_obj_members(obj)]

def get_obj_attr_vals(obj,notcallable=True):
    return [val for _,val,callable in get_obj_members(obj) if callable == False]
        
def get_obj_attr(obj,notcallable=True):
    return [(_name,_val) for _name,_val,callable in get_obj_members(obj) if callable == False]
                
class generic:
    def __init__(self,**args):
        for key,value in args.iteritems():
            setattr(self,key,value)
            
        self.__get_attr__ = get_obj_attr
        self.__get_attr_names__ = get_obj_attr_names

    def __print_attr__(self):
        for attrname,attrval in self.get_attr():
            print attrname,attrval

class enum(generic):
    pass

def gettype(string):
    try:
        return(int(string))
    except:
        try:
            return(float(string))
        except:
            return(string)
    
def write_text_to_file(filename,text):
    fh = open(filename,'w+')
    fh.write(text)
    fh.close
    


def read_text_from_file(filename,delim=","):
    '''returns a list of elements; converts to int if it can'''
    filel=[]
    fh = open(filename, 'r+')
    for line in fh:
        l=[]
        for element in line.rstrip().split(delim):
            l.append(gettype(element))

        filel.append(l)
    return(filel)

def file2string(filename):
    '''returns a string'''
    s=""
    fh = open(filename, 'r+')
    
    for line in fh:
        s+=line
    return s

def read_delim_text_from_file(filename,delim):
    'returns a list of lists'
    l=[]
    fh = open(filename, 'r+')
    
    #for line in fh:
    #    l.append(line.rstrip().split(delim))
    #        
    #return l

    return [l.append(line.rstrip().split(delim)) for line in fh]

def print_dict_of_dict(d):
    ''' takes a dict of dicts an input like :
    
    {'abc': {'a': 1, 'c': 3, 'b': 2}, 'ghi': {'a': 7, 'c': 9, 'b':8}}
    
    and prints a bordered grid in the below format:
    
    |--------------------|--------------------|--------------------|
    |         a          |         c          |         b          |
    |--------------------|--------------------|--------------------|
    |         1          |         3          |         c          |
    |         7          |         9          |         8          |
    |--------------------|--------------------|--------------------| '''
       
    def _print_hz_BORDER(num_cols): 
        ''' prints a horizontal border of the form :
        |--------------------|--------------------|--------------------| '''
        out_str= VZ_BORDER
        for i in range(num_cols):
                out_str += ULINE.ljust(PAD,ULINE)+VZ_BORDER
        print(out_str)
        
    PAD=20
    VZ_BORDER="|"
    ULINE="-"
    
    num_keys = len(d[d.keys()[0]].keys())
        
    # ensure table starts on a new line
    print
        
    # print top VZ_BORDER for column names/table
    _print_hz_BORDER(num_keys)
            
    # print column names
    out_str = VZ_BORDER
    for key in d[d.keys()[0]].keys():
        out_str += str(key).center(PAD) + VZ_BORDER
    print(out_str)
        
    # print bottom VZ_BORDER for column names
    _print_hz_BORDER(num_keys)

    # print values
    for key1 in d.keys():
        out_str= VZ_BORDER
        for key2,val2 in d[key1].iteritems():
            out_str += str(val2).center(PAD)+VZ_BORDER
        print(out_str)
    
    # print bottom VZ_BORDER for table
    _print_hz_BORDER(num_keys)
    
    # ensure blanl line between table and any additional output
    print
    

class Singleton(type):
    '''
    this is to be used as a __metaclass__
    __metaclass__ = Singleton
    '''
    _instances = {}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)

        return cls._instances[cls]
    
    
    
    #path.append("/Users/burtnolej/Dev/pythonapps/util")
    #from misc_util import write_object_to_disk,read_object_from_disk,Singleton
    #from os import path as ospath

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
        
