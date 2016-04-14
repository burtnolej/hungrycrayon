#!/usr/bin/python


import threading
import Queue
import time

myQueue = Queue.Queue()

class count_stuff(threading.Thread):

    def __init__(self,start_num,end, q):
        self.num = start_num
        self.end = end
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self.num != self.end:
                self.num += 1
                self.q.put(str(self.num)+str(self))
                #print "Outputting: ",str(self.num)
                time.sleep(5)
            else:
                break

#class my_stuff(threading.Thread):

#    def __init__(self):
#        print "XYZ"
#        threading.Thread.__init__(self)

#    def run(self):
#        pass
    
myThread = count_stuff(1,10,myQueue)
myThread.start()
myThread = count_stuff(1,10,myQueue)
myThread.start()
myThread = count_stuff(1,10,myQueue)
myThread.start()

#ms = my_stuff()
#ms.start()

while True:
    if not myQueue.empty():
        val = myQueue.get()
        print "Outputting: ",val
    time.sleep(2)
