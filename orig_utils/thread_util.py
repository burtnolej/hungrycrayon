#!/usr/bin/python

from sys import path, argv, stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Logger
from misc_util import in_method_log_lite as im_log
from datetime_util import MyDT
from inspect import getmembers
import threading
import time
from Queue import Queue
from multiprocessing.pool import ThreadPool

threadLock = threading.Lock()
def _lock(func):
    def _tmp(*args, **kw):
        with threadLock:
            func(*args, **kw)
    return _tmp

class QueueMessage(object):
    def __init__(self,reader,**kwargs):
        for key,value in kwargs.iteritems():
            setattr(self,key,value)
        self.recipient = reader

    @_lock
    def pprint(self,action,owner):
        print "action".ljust(10),action
        print "owner".ljust(10),owner
        for key,value in getmembers(self):
            if not str(key).startswith("__") and not callable(value):
                print key.ljust(10),value
        print

class MyThread(threading.Thread):
    myQueue = Queue()
    threads = {}

    #@im_log()
    def __init__(self, tname,*args,**kwargs):
        threading.Thread.__init__(tname)
        self.name = tname
        self.kwargs = kwargs
        self.args = args
        
    @classmethod
    def expfunc(cls, tname, func, **kwargs):
        cls1 = cls(tname,**kwargs)
        cls1.func = func
        return(cls1)

    @classmethod
    def clsobj(cls,tname,*args,**kwargs):
        print args
        cls1 = cls(tname,*args,**kwargs)
        cls1.func = cls1.run
        return(cls1)

    @staticmethod
    def check_q_exec(name,func):
        '''
        check for a message for name. if yes execute func using the
        value (payload) on the message as an argument
        ''' 
        qm = MyThread.myQueue.get()
        qm.pprint("get",name)
        if qm.recipient == name:
            func(qm.payload)
        else:
            MyThread.myQueue.put(qm)

    @staticmethod
    def check_q(name):
        '''
        check for a message for name. if yes return the value(payload)
        '''
        qm = MyThread.myQueue.get()
        qm.pprint("get",name)
        if qm.recipient == name:
            return(qm.payload)
        else:
            MyThread.myQueue.put(qm)
            return False

    @im_log()
    def run(self):
        type(self).threads.__setitem__(self.name,"")
        self.func(*self.args,**self.kwargs)
        type(self).threads.__delitem__(self.name)

    @staticmethod
    def active_threads():
        l = len(type(self).threads)
        if l > 0:
            return True
        return False

    @staticmethod
    def atc_check(l=None):
        atc = type(self).active_thread_count()
        if not l: l = stdout
    
        if atc == 0:
            return False
        return True

    @staticmethod
    def active_thread_count():
        return(len(threads))
        
if __name__ == '__main__':

    def func(duration):
        time.sleep(duration)

    # Create new threads
    #thread1 = MyThread.expfunc("Thread-1",func,duration=2)
    #thread2 = MySubClassThread.clsobj("Thread-2",duration=10)

    # Start new Threads
    #thread1.start()
    #thread2.start()

    #while atc_check():
    #    time.sleep(0.05)

    class MyQueueWriter(MyThread):
        def run(self,reader_list,interval):
            for reader in reader_list:
                qm = QueueMessage(reader,sender=self.name,payload=MyDT(display_fmt='%H:%M:%S'))
                with threadLock:
                    MyThread.myQueue.put(qm)
                qm.pprint("put",self.name)
                time.sleep(interval)


    class MyQueueReader(MyThread):
        def run(self,action):
            while not self.read_q():
                time.sleep(1)

        def read_q(self):
            qm = MyThread.myQueue.get()
            if qm.recipient == self.name:
                qm.pprint("get",self.name)
                return True
            else:
                qm.pprint("miss",self.name)
                MyThread.myQueue.put(qm)
                return False


    writer = MyQueueWriter.clsobj("w",reader_list=["r5","r2","r3","r1"],interval = 1)
    reader1 = MyQueueReader.clsobj("r1",action=1)
    reader2 = MyQueueReader.clsobj("r2",action=2)
    reader3 = MyQueueReader.clsobj("r3",action=3)

    writer.start()
    reader1.start()
    reader2.start()
    reader3.start()

    while MyThread.atc_check():
        time.sleep(0.5)
        #print "queue size",myQueue.qsize()

    

    
