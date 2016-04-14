#!/usr/bin/python

from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
import threading
import Queue
import time
import curses
from misc_util import Logger, in_method_log

myQueue = Queue.Queue()

class WinCharListener(threading.Thread):
    def __init__(self,win):
        threading.Thread.__init__(self)
        self.win_ref = win
        
    def run(self):
        while True:
            event = self.win_ref.getch()
            if event == ord('q'):
                break
            else:
                #self.win_ref.addstr(2,1,chr(event))
                self.win_ref.addstr(chr(event))
                self.win_ref.refresh()
            
class WinQListener(threading.Thread):

    def __init__(self,start_num,end,q,win):
        threading.Thread.__init__(self)
        self.num = start_num
        self.end = end
        self.q = q
        self.win_ref = win

    @in_method_log
    def add_to_q(self,item):
        self.q.put(item)

    @in_method_log
    def write_to_win(self,y,x,text):
        self.win_ref.addstr(y,x,text)
        self.win_ref.refresh()

    @in_method_log
    def counter(self):
        if self.num != self.end:
            self.num += 1
            return True
        return False
            
    def run(self):
        while self.counter():
            self.add_to_q(str(self.num)+str(self))
            self.write_to_win(1,1,str(self.num))
            time.sleep(1)

class Win():
    def __init__(self,sy,sx,y,x,screen):
        #self.win_ref = screen.subwin(sy,sx,y,x)
        self.win_ref = curses.newwin(sy,sx,y,x)
        self.win_ref.border()

        self.init_threads()

    def init_threads(self):
        pass

    
class WinQ(Win):
    def init_threads(self):
        wql = WinQListener(1,10,myQueue,self.win_ref)
        wql.start()

class WinChr(Win):
    def init_threads(self):
        wcl = WinCharListener(self.win_ref)
        wcl.start()

def main(screen):
    l = Logger()
    
    screen.keypad(1)
    curses.mousemask(1)

    wq = WinChr(5,30,20,5,screen)
    #wc = WinQ(5,30,5,5,screen)


    while True:
        pass
        #if not myQueue.empty():
            #pass
            #val = myQueue.get()
            #wc.win_ref.addstr(2,1,val)
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print "Got KeyboardInterrupt exception. Exiting..."
        exit()
