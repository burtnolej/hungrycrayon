#!/usr/bin/python

import inspect
from sys import exc_info, exit,path

path.append("/Users/burtnolej/Dev/pythonapps/util")

from linecache import getline
from os import path
import traceback
from table_print import SimpleTable
from misc_util import Logger

'''
todo : need to modify table_print to expand lists so recurse if list contains objects
'''

class FrameRecord():
    '''
    simple class to represent a frame
    '''
    _list = []
    _key_list = ['frame_object','filename','line_no','function_name','source_lines','current_line_index']
            
    def __init__(self,frame_record):
        self.convert_list_to_object(frame_record)
        self.locals = self.frame_object.f_locals
        self._list.append(self)
        #print "created FrameRecord instance",self

    def convert_list_to_object(self,frame_record):
        assert (len(frame_record) == len(self._key_list))
        
        [setattr(self,self._key_list[i],frame_record[i]) for i in range(0,len(self._key_list))]
        
    def pprint(self):
        for key,value in inspect.getmembers(self):
            if not str(key).startswith("__"):
                if not callable(value):
                    if not isinstance(value,(list,dict,tuple)):
                        print key.rjust(15),value        

def clear_list():
    FrameRecord._list = []
    return(len(FrameRecord._list))
           

def convert_list_to_dict(key_list,value_list):
    '''
    take a list containing key names and a list containing values
    this is just to help readability
    '''
    assert (len(key_list) == len(value_list))
    assert isinstance(key_list,(list,tuple))
    assert isinstance(value_list,(list,tuple))

    return({key_list[i]:value_list[i] for i in range(0,len(key_list))})

def get_exception_info():
    '''
    returns info about the exception that is currently being handled
    info is specific to the current thread and the current stack frame
    'handling an exception' means a stack frame that is executing an
    an except clause
    
    returns in a dict so easy to read and self documenting

    type : (class object) exception type of the exception being handled
    value : (class instancwe) the exception parameter (its associated
    value of the 2nd arg to raise which is always a class instance
    traceback (traceback object) : encapsulating the call stack at the
    point where the exception originally occured
    '''
    l=exc_info()
    return(convert_list_to_dict(['type','value','traceback'],l))

    ###### from here need to populate FrameRecords from traceback...

def get_inner_frames(traceback=None):
    '''
    get a list of frame records for a tracebacks frame and all inner
    frames. these frames represent the calls that lead to the creation
    of the last frame
    args:   traceback object of exception to use
            None to denote use current exception
    return: None
    '''
    if traceback == None:
        traceback = get_exception_info().__getitem__("traceback")
    assert inspect.istraceback(traceback)
        
    [FrameRecord(fr) for fr in inspect.getinnerframes(traceback)]
    
    ei = get_exception_info()
    for fr in FrameRecord._list:
        fr.error_type = ei.__getitem__("type")
        fr.error_value = ei.__getitem__("value")
        #fr.error_msg = fr.error_value.message
    

def get_outer_frames(frame=None):
    '''
    get a list of frame records for a tracebacks frame and all inner
    frames. these frames represent the calls that lead to the current frame
    '''
    if frame == None:
        frame = inspect.currentframe()
        
    assert inspect.isframe(frame)
    [FrameRecord(fr) for fr in inspect.getouterframes(frame)]

def get_stack():
    '''
    populate class FrameRecord with the current stack
    '''
    [FrameRecord(fr) for fr in inspect.stack()]
    return(FrameRecord)

def get_number_of_frame_records():
    return(len(FrameRecord._list))
               
def get_source_lines():

    if get_number_of_frame_records() == 0:
        get_stack()

    for fr in FrameRecord._list:
        print str(fr.filename).ljust(20), str(fr.line_no).ljust(20),str(fr.source_lines).ljust(20)

class MyException(Exception):
    message = "this is an error message"
    
def c():
    raise MyException
    
def b():
    c()
    
def a():
    b()

def tmp_print(object,text):
    SimpleTable(object,0,3,2,False,False,"",text).deep_print()
    
if __name__ == '__main__':

    l = Logger("/private/tmp/log.txt",True)

    get_stack()   
    tmp_print(FrameRecord,"STACK")
    clear_list()

    try:
        a()
    except MyException:
        get_inner_frames()
        tmp_print(FrameRecord,"INNER FRAME FROM AN EXCEPTION")
        clear_list()
        
    get_outer_frames()
    tmp_print(FrameRecord,"OUTER FRAME")
    clear_list()
     
    del(l)
