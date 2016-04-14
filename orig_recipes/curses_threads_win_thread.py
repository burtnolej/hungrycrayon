#!/usr/bin/python

from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
import threading
import Queue
import time
import curses
from misc_util import Logger, in_method_log

myQueue = Queue.Queue()
lock = threading.Lock()
    
class Win(threading.Thread):
    def __init__(self,sy,sx,y,x,screen):
        self.win_ref = screen.subwin(sy,sx,y,x)
        self.win_ref.border()
        self.win_ref.refresh()
        threading.Thread.__init__(self)

    def write_to_win(self,text,y=None,x=None):
        with lock:
            if y==None and x==None:
                self.win_ref.addstr(text)
            else:
                self.win_ref.addstr(y,x,text)
            self.win_ref.refresh()

class WinCharListener(Win):
    def run(self):
        while True:
            event = self.win_ref.getch()
            if event == ord('q'):
                break
            else:
                self.write_to_win(chr(event))
            
class WinQListener(Win):
    def __init__(self,*args):
        super(WinQListener,self).__init__(*args)
        self.num = 1
        self.end = 10
        self.q = myQueue

    @in_method_log
    def add_to_q(self,item):
        self.q.put(item)

    @in_method_log
    def counter(self):
        if self.num != self.end:
            self.num += 1
            return True
        return False
            
    def run(self):
        while self.counter():
            self.add_to_q(str(self.num)+str(self))
            self.write_to_win(str(self.num),1,1)
            time.sleep(0.5)

def main(screen):
    screen.keypad(1)
    curses.mousemask(1)

    wq = WinCharListener(5,25,22,2,screen)
    wq.start()

    wq2 = WinCharListener(5,25,12,32,screen)
    wq2.start()

    wq3 = WinCharListener(5,25,12,2,screen)
    wq3.start()        

    wc = WinQListener(5,25,2,32,screen)
    wc.start()
    
    wc2 = WinQListener(5,25,2,2,screen)
    wc2.start()

    wq3.join()
    wc2.join()
    
if __name__ == '__main__':
    l = Logger()
    try:
        curses.wrapper(main)
    except:
        del l
        exit()
