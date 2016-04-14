#!/usr/bin/python

__all__ = ["get_log_handle","get_error_type","get_log_handle","get_log_name",
    "get_pid","get_userid","print_object",
    "print_list","print_dict","print_headline_table","print_function_result_table","print_locals",
    "print_module_init_msg","get_current_filename","get_calling_function","print_stack",
    "get_object_name","get_date_dmy","get_time_hms","get_time_secs",
    "switch","switch","get_exec_info",
    "bracket","quote","get_terminal_size","write_object_to_disk"]

from os import getpid
from os import getlogin, path
from inspect import stack
from time import strftime
from time import time
import datetime
from sys import exc_info
from sys import stdout,stderr
from collections import OrderedDict
from linecache import getline
from itertools import product
import threading
import traceback
from linecache import getline

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

class Singleton(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)
        return cls._instances[cls]

def in_method_log(lh):
    import sys
    # need to assert that lh is a file handle
        
    def actual_dec(func):
        def _logged(*args, **kw):
        
            lh.write(str(get_time_hms()).ljust(12))
            lh.write(":a:")
            lh.write(str(func.__name__).ljust(20))
            lh.write(str(args).ljust(20))
            lh.write(str(kw).ljust(20))
            lh.write("\n")

            result = func(*args, **kw)
        
            lh.write(str(get_time_hms()).ljust(12))
            lh.write(":r:")
            lh.write(str(func.__name__).ljust(20))
            lh.write(str(result).ljust(30))
            lh.write("\n")
            
            return result
        return _logged
    return actual_dec

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
    
    def match(self, *args):
        if self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        elif self.fall or not args:
            return True
        else:
            return False

def file2list(filename):
    l=[]
    fh = open(filename, 'r+')
    return [line.rstrip() for line in fh]
 
def write_object_to_disk(object,filename=None):
    import pickle
    if filename == None:
        filename = get_log_name(".dat")
    filehandler = open(filename, 'w') 
    pickle.dump(object, filehandler)
    return(filename)

def read_object_from_disk(filename):
    import pickle
    filehandler = open(filename, 'r') 
    object = pickle.load(filehandler) 
    return(object)

class Logger():
    '''
    optional arg filename : to specify filename to use
    this is useful if you just want to write to say 'log.txt'
    rather than a diff name each time
    
    optional arg overwrite : to specific overwrite to filename or append if log filename already exists
    '''
    import sys
    def __init__(self,filename=None,overwrite=True):
        
        if filename != None:
            self.log_name = filename
        else:
            self.log_name = get_log_name()

        self.err_log_name = self.log_name + ".err"
                
        self.log_handle = get_log_handle(self.log_name,overwrite) # opens log
        self.err_log_handle = get_log_handle(self.err_log_name,overwrite) # opens log

        # redirect std.out to the logfile
        self.tmp_stdout = self.sys.stdout # store std.out to reset back to
        self.tmp_stderr = self.sys.stderr # store std.err to reset back to
        self.sys.stdout = self.log_handle
        self.sys.stderr = self.err_log_handle

    def __del__(self):
        self.sys.stdout = self.tmp_stdout # reset std.out back to screen
        self.sys.stderr = self.tmp_stderr # reset std.err back to screen
        del_log_handle(self.log_handle) # close logfile
        del_log_handle(self.err_log_handle) # close logfile
        #del self.sys

        import os
        print self.log_name + " (" + str(os.stat(self.log_name).st_size) + " bytes)"
        print self.err_log_name + " (" + str(os.stat(self.err_log_name).st_size) + " bytes)"


    def write(self,text,err=True):
        
        if err:
            self.err_log_handle.write(text)
            self.err_log_handle.flush()
        else:
            self.log_handle.write(text)
            self.log_handle.flush()


def bracket(text):
    return("("+str(text)+")")

def quote(text):
    return("'"+str(text)+"'")

def get_error_type():
    etype,foo, traceback = exc_info()
    return(etype)

def write_to_file(filename,text):
    fh = open(filename,'w+')
    fh.write(text)
    fh.close
    
def get_log_handle(logname = None,overwrite=True):
   
    if logname == None:
        logname = get_log_name()

    if overwrite:
        return(open(logname, 'w+'))
    else:
        return(open(logname, 'a+'))
        
def get_log_name(suffix=".log"):
    filename = get_current_filename()
    date_dmy = get_date_dmy()
    time_hms = get_time_hms()

    _log_name = "/tmp/" + filename + "_" + str(get_pid()) + "_" + get_userid() + "_" + date_dmy + "_" + time_hms + suffix

    return (_log_name)

def del_log_handle(log_name):
    log_name.close()

def get_pid():
    return(str(getpid()))

def get_userid():
    return(getlogin())

    
def print_locals(mylocals):
    print_dict(mylocals)

def get_current_filename():
    import __main__ as main
    if hasattr(main,"__file__"):
        return(main.__file__)
    else:
        return("shell")
 
def get_calling_function(level = None):
    # get the penultimate command in the stack
    if level == None:
        return(stack()[1][3])
    else:
        return(stack()[level][3])

def print_stack():
    # print the entire stack
    print_list(stack())

def get_object_name(myself):
    return(get_stripped_name(myself))

def get_date_dmy():
    return(datetime.now().strftime("%d-%m-%y"))

def get_time_hms():
    return(datetime.now().strftime("%H:%M:%S"))

def get_time_secs():
    return(time())

def datetime_to_secs(dt):
    '''
    understands "dd/mm/YYYY H:M:S"
    '''
    assert len(dt.split()) == 2
    cd,ct = dt.split()

    assert len(cd.split("/")) == 3
    assert len(dt.split(":")) == 3
    d,mt,y = cd.split("/")
    h,m,s = ct.split(":")

    origin  = datetime.datetime(1970,1,1,0,0,0)
    mydt = datetime.datetime(int(y),int(mt),int(d),int(h),int(m),int(s))
    return(int((mydt-origin).total_seconds()))

def date_to_secs(date):
    '''
    understands "dd/mm/YYYY"
    '''
    assert len(date.split("/")) == 3
    d,mt,y = date.split("/")
    h,m,s = 12,1,1

    origin  = datetime.datetime(1970,1,1,0,0,0)
    mydate = datetime.datetime(int(y),int(mt),int(d),int(h),int(m),int(s))
    return(int((mydate-origin).total_seconds()))

def secs_to_datetime(secs):
    '''
    returns "dd/mm/YYYY H:M:S"
    '''
    return(datetime.datetime.utcfromtimestamp(secs).strftime('%d/%m/%Y %H:%M:%S'))
    
def print_dict_basic(d):
        for key,value in d.iteritems():
            print '{:<20}'.format(key),
            print ':{:<5}'.format(value),
            print

def set_config_dict(**kwargs):
    return {key:value for key,value in kwargs.iteritems()}
            
def compare_arrays(a,b):
    '''
    A B     Take two lists a and b and compares them item by item 
    1 6->6  taking the largest each time.
    6 1->6
    '''
    if len(a) != len(b):
        print "ERROR - len listA: " + str(len(a)) + "len listB: " + str(len(b)) + " - need to be the same length"
        raise ValueError
        
    return[a[i] if a[i] > b[i] else b[i] for i in range(0,len(a))]

def items_allsame_length(items):
    return all(len(x) is len(items[0]) for x in items)

def get_terminal_size():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

def get_exec_info():
    exc_type, exc_obj, exc_tb = exc_info()
    fname = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    line = getline(fname, exc_tb.tb_lineno)
    return(exc_type,exc_obj,exc_tb.tb_lineno,line,fname)

class TestSuperClass(object):
    test_super = "im here"
    test_super2 = "im here 2"

class TestClass(TestSuperClass):
    test_int = 1
    test_class = switch
    test_object_instance = _GetchUnix()
    test_function = stack
    test_error = IndexError
    test_list = ['ipsum']
    test_dict = {'ipsum':'decorum'}
    test_object_instance_method = _GetchUnix.__init__
    test_object_instance_var = test_int

if __name__ == '__main__':
    while 1:
        user_input = raw_input("\nPlease enter test ('help' for help) : ")

        for case in switch(user_input):
            if case('get_time_hms'):
                print_function_result_table('get_time_hms()')
                break
            if case('help'):
                print __all__
                break
            if case('get_date_dmy'):
                print_function_result_table('get_date_dmy()')
                break
            if case('get_time_secs'):
                print_function_result_table('get_time_secs()')
                break
            if case('get_object_name'):
                class myclass():
                    def __init__(self):
                        self._myvar = "myvarval"
                _myclass = myclass()

                print_function_result_table('get_object_name("'+str(myclass())+'")')
                break
            if case('write_object_to_disk'):
                filename = write_object_to_disk(TestClass)
                object = read_object_from_disk(filename)
                print "object:%s file:%s type:%s" % (object,filename,object.__name__)
                break 
            if case('get_calling_function'):
                print_function_result_table('get_calling_function()')
                print_function_result_table('get_calling_function(2)')
                break
            if case('read_char'):
                getch = _GetchUnix()
                getch()
                break
            if case('print_locals'):
                print_locals(locals())
                break
            if case('get_current_filename'):
                print_function_result_table('get_current_filename()')
                break
            if case('get_pid'):
                print_function_result_table('get_pid()')
                break
            if case('get_userid'):
                print_function_result_table('get_userid()')
                break
            if case('Logger'):
                logger = Logger()
                logger.write("this is a test")
                print "see: " + logger.log_name
                break
            if case('get_terminal_size'):
                print get_terminal_size()
                break
            if case('print_module_init_msg'):
                print_module_init_msg(locals())
                break
            if case('print_stack'):
                print_stack() 
                break
            if case('get_error_type'):
                try:
                    int("a")
                except:
                    print get_error_type()
                    break
            if case('get_exec_info'):
                print "see 'ErrorTable'"
                break
            if case():
                print "no test implemented" 
