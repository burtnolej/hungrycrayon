#!/usr/bin/python

from sys import path, argv, stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Logger
from misc_util import in_method_log_lite as im_log
from datetime_util import MyDT
from inspect import getmembers
from threading import Thread, Lock
import time
from Queue import Queue
from multiprocessing.pool import ThreadPool

threadLock = Lock()
def _lock(func):
    def _tmp(*args, **kw):
        with threadLock:
            func(*args, **kw)
    return _tmp

class MyQueueWriter(Thread):

    def __init__(tname,*args,**kwargs):
        Thread.__init__(tname)

    def run(self,reader_list,interval):
        for reader in reader_list:
            qm = QueueMessage(reader,sender=self.name,payload=MyDT(display_fmt='%H:%M:%S'))
            with threadLock:
                MyThread.myQueue.put(qm)
            qm.pprint("put",self.name)
            time.sleep(interval)


class MyQueueReader(Thread):

    def __init__(tname,reader_list,interval):
        self.tname = tname
        self.reader_list = reader_list
        self.interval = interval
        
        Thread.__init__(tname)

    def run(self):
        while not self.read_q():
            time.sleep(1)

    def read_q(self):
        qm = MyThread.myQueue.get()
        if qm.recipient == self.tname:
            qm.pprint("get",self.tname)
            return True
        else:
            qm.pprint("miss",self.name)
            MyThread.myQueue.put(qm)
            return False

if __name__ == '__main__':
    
    writer = MyQueueWriter("w",reader_list=["r5","r2","r3","r1"],interval = 1)
    reader1 = MyQueueReader("r1",action=1)
    reader2 = MyQueueReader("r2",action=2)
    reader3 = MyQueueReader("r3",action=3)

    writer.start()
    reader1.start()
    reader2.start()
    reader3.start()

    while MyThread.atc_check():
        time.sleep(0.5)
        #print "queue size",myQueue.qsize()

    

    
