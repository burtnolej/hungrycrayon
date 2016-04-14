#!/usr/bin/python

'''
programe to read keypresses nd write to an event bus
'''

import threading
import Queue
import time

import termios, fcntl, sys, os
myQueue = Queue.Queue()


class keyboard_listener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            while 1:
                try:
                    c = sys.stdin.read(1)
                    print "Got character", repr(c)
                    if c == 'q':
                        exit()
                except IOError: pass
        finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
                fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



myThread = keyboard_listener()
myThread.start()
#myThread = count_stuff(1,10,myQueue)
#myThread.start()
#myThread = count_stuff(1,10,myQueue)
#myThread.start()
#myThread = count_stuff(1,10,myQueue)
#myThread.start()

#ms = my_stuff()
#ms.start()

#i=0
#while not myQueue.empty():
#    val = myQueue.get()
#    print "Outputting: ",val,myQueue.qsize()
#    time.sleep(0.2)
