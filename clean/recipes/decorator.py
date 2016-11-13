
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import Log
from time import time, sleep

log = Log()

from inspect import stack

def _func(cls=None):
    
    funcname = stack()[1][3]
    
    if cls <> None:
        clsname = cls.__class__.__name__
        funcname = clsname + "." + funcname
    
    return(funcname)

def logger(log):

    def decorator(func):
        def wrapper(*args, **kw):
            stime = time()
            log.log(func.__name__,100,args=args,kw=kw)
            result = func(*args, **kw)
            etime = round(time()-stime,4)
            log.log(func.__name__,101,etime=etime,result=result)
            return result
        return wrapper
    return decorator

class myclass(object):
    def __init__(self):
        log.log(_func(self),3)
    
    @logger(log)
    def memberfunc(self,args):
        log.log(_func(self),3)
        
    @logger(log)
    def wait(self):
        sleep(0.1555)
        log.log(_func(self),3)
        
            
@logger(log)
def func1(*args,**kwargs):
    log.log(_func(),3,foo='baa')
    return(100)


mc = myclass()
mc.memberfunc("foobar")
mc.wait()
func1("abc","xyz")

print log.stats