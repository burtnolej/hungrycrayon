
import sys

from misc_utils import Singleton, thisfuncname
from misc_utils_process import process_instances_get, process_kill, process_start, process_get_stdout, \
     process_stdin
from time import time, sleep
from inspect import stack
from os.path import basename
from datetime import datetime
from threading import currentThread
from collections import OrderedDict
import os
import os.path
from types import *

def logger(log):
    
    def decorator(func):
        def wrapper(*args, **kw):
            stime = time()
            funcname = ".".join(([func.__module__,func.__name__]))
            
            # explicitly pass in func args with fargs/fkw keywords
            log.log(funcname,11,fargs=args,fkw=kw)
            result = func(*args, **kw)
            etime = round(time()-stime,4)
            log.log(funcname,12,etime=etime,result=result)
            return result
        return wrapper
    return decorator

class Log():
    __metaclass__ = Singleton
    
    def __init__(self,
                 cacheflag=False,
                 logdir=None,
                 verbosity=5,
                 pidlogname=True,
                 proclogname=True):
        self.cache = []
        self.cacheflag = cacheflag
        self.logdir = logdir
        self.verbosity = verbosity
        self.stats = {}
        
        if self.logdir == None:
            self.logdir = '/home/burtnolej/log'
            print "no log dirname provided so defaulting to",self.logdir
        
        if os.path.isdir(logdir) == False:
            print "creating directory",self.logdir
            os.mkdir(logdir)

        self.logpath = os.path.join(self.logdir,"log")
        
        # add the calling process to the log file name
        if proclogname == True:
            self.logpath = self.logpath + "." + basename(stack()[2][1])
        
        # add the PID to the log filename
        if pidlogname == True:
            self.logpath = self.logpath + "." + str(self._getpid())
            
        print "using logfile:",self.logpath
        fileattr = "a"
        if os.path.exists(self.logpath) == False:
            self.log(self.__init__,3,msg="creating logfile",name=self.logpath)
            fileattr = "w"
        
        self.logfile = open(self.logpath,fileattr)
        
        self.log(self.__init__,3,logdir=self.logdir,verbosity=verbosity,pidlogname=str(pidlogname),
                 proclogname=str(proclogname))

    def verbosity_set(self,new_value):
        self.log(thisfuncname(),3,msg="updating verbosity",old_value = self.verbosity,new_value = new_value)
        self.verbosity = new_value
        
    def _getpid(self):
        thread = currentThread().name
        if thread == 'MainThread':
            return(os.getpid())
        return(thread)
        
    def __repr__(self):
        return ('log')
    
    def log_cache_reset(self):
        self.cache=[]
        
    def log_cat(self,grepargs=[]):

        self.logfile.close()        

        cmd = ["cat",self.logpath]
        p = process_start(cmd)
        logfile = process_get_stdout(p) 
        
        print        
        if grepargs <> []:
            cmd = ['grep'] + grepargs      
            p = process_start(cmd,stdin=True)
            
            for line in process_stdin(p,logfile):
                print line
        else:
            print logfile
          
    def _args_readable(self,args):
        ''' if the args contain fill object names like <module 'os' from '/usr/local/lib/python2.7/os.pyc'>
        make it more readable like os.pyc '''
        if type(args) is TupleType:
            for arg in args:
                if type(arg) not in [TupleType, StringType, IntType,DictionaryType,ListType, FloatType]:
                    newarg = arg.__class__.__name__
                    args = list(args)
                    args.remove(arg)
                    args.insert(0,newarg)
        
        elif type(args) is DictType:
            for k,v in args.iteritems():
                if type(v) not in [TupleType, StringType, IntType,DictionaryType,ListType, FloatType]:
                    if type(v) in [FunctionType,MethodType]:
                        newarg = v.__name__
                        args[k] = newarg
                    else:
                        try:
                            newarg = v.__name__
                        except:
                            newarg = v.__class__.__name__
                            
                        args[k] = newarg
                        
        return(args)
        
    def log(self,funcname,priority,**kwargs):

        try:
            int(priority)
        except:
            raise Exception('priority arg needs to be an int, got',priority)
 
        callerframe = stack()[1]
    
        config = OrderedDict([('now',12),('thread',6),('type',8),('module',20),('funcname',30),('etime',6),('result',10),('fargs',20),('fkw',20),('logmesg',-1)])

        logmesg = OrderedDict()
        
        # get the thread PID
        logmesg['thread'] = str(self._getpid())   
        
        # set up stats for this PID and create a ref to use
        if self.stats.has_key(logmesg['thread']) == False:
            _stats = self.stats[logmesg['thread']] = dict(etime=0)
        else:
            _stats = self.stats[logmesg['thread']]
            
        # is this message of a sufficient priority to make it to the log instance
        if priority < self.verbosity or priority >= 100:
            logitem = []
            
            logmesg['funcname'] = funcname
            logmesg['module'] = basename(stack()[1][1])

            # setup stats for this given function if not called before
            if _stats.has_key(logmesg['funcname']) == False:
                _stats[logmesg['funcname']] = dict(no=0,etime=0)

            if priority == 100: # decorator start of function
                logmesg['type'] = "INFUNC"
                
                # pull out the args passed to the function
                fkw =kwargs['fkw']
                fargs = self._args_readable(kwargs['fargs'])
                
                # make them readable and put on to the output logmesg
                logmesg['fkw'] = str(zip(map(str,fkw.keys()),map(str,fkw.values())))
                logmesg['fargs'] = ",".join(map(str,fargs))
                
                # remove spaces to make output more searchable/testable
                logmesg['fargs'] =  logmesg['fargs'].replace(" ","").strip()
                logmesg['fkw'] =  logmesg['fkw'].replace(" ","")
                
                # remove of kwargs leaving only other info that needs to go to the log
                kwargs.pop('fkw')
                kwargs.pop('fargs')    

            elif priority == 101: # decorator end of function
                
                # add stats and build mesg
                _stats['etime'] += kwargs['etime']
                _stats[logmesg['funcname']]['etime'] += kwargs['etime']
                _stats[logmesg['funcname']]['no'] += 1
                
                logmesg['type'] = "OUTFUNC"
                logmesg['etime'] = str(kwargs['etime'])
                logmesg['result'] = str(kwargs['result'])
                
                # remove of kwargs leaving only other info that needs to go to the log
                kwargs.pop('etime')
                kwargs.pop('result')
            else:

                if priority in [4]:
                    logmesg['type'] ="SUCCESS"                
                elif priority in [3]:
                    logmesg['type'] ="INFO"
                elif priority in [7,8,9]:
                    logmesg['type'] ="DEBUG"
                elif priority in [1]:
                    logmesg['type'] = "ERROR"
                elif priority in [0]:
                    logmesg['type'] = "FATALERROR"
                    
                elif priority in [2]:
                    logmesg['type'] = "FAILURE"
                else:
                    logmesg['type'] ="UNKNOWN"
            
            now = datetime.now().strftime("%H:%M:%S")
            
            logmesg['now'] = ":".join(map(str,[now,datetime.now().microsecond/1000]))
            
            # add into logmesg any other info passed into the log function as kwargs
            kwargs = self._args_readable(kwargs)
            logmesg['logmesg'] = str(zip(map(str,kwargs.keys()),map(str,kwargs.values())))
            #logmesg['logmesg'] =  logmesg['logmesg'].replace(" ","")
            
            # build log mesg as specified in config
            output = []
            for name,size in config.iteritems():
                if logmesg.has_key(name):
                    if size != -1:
                        if logmesg[name] <> None:
                            s = self.shrink(str(logmesg[name]),size)
                            output.append(s.ljust(size))
                        else:
                            output.append("None".ljust(size))
                    else:
                        output.append(logmesg[name])
                else:
                    output.append("".ljust(size))
            
            # keep copy of log messages in memory if specified
            if self.cacheflag == True:
                self.cache.append(output)
            
            # in case the file has been closed
            try:
                self.logfile = open(self.logpath,"a")
            except IOError:
                pass

            self.logfile.write("|".join(output)+"\n")
            self.logfile.flush()
            
            if logmesg['type'] == "FATALERROR":
                print "FATAL ERROR, exiting; check logs"
                exit()
                
            
    def shrink(self,s,size):
        ''' pull out middle chars to fit into desired width of log field '''
        if len(s) > size:
            _len = size/2
            s = s[:_len-1] + "*" +s[len(s)-_len:]
        return(s)

    def log_get_session_content(self):
        return(self.cache)
    
    def log_delete(self):
        os.remove(self.logpath)
            
    def log_clean(self):
        self.log_null()
        self.log_cache_reset()
        
    def log_null(self):
        try:
            self.logfile = open(self.logpath,"a")
        except IOError:
            pass
        
        cmd = ["nullfile.sh",self.logpath]
        p = process_start(cmd)  
        
        self.logfile.close()
        
    def logexists(self):
        return(os_file_exists(self.logpath))

    def log_get_session_num_entries(self):
        return(len(self.cache))
    
    def log_file_length(self):
        try:
            self.logfile = open(self.logpath,"r")
        except IOError:
            pass
        for i,l in enumerate(self.logfile):
            pass
        self.logfile.close()
        return(i)

    def __del__(self):
        self.logfile.close()
