from time import sleep
import os

def child():
    
    for i in range(10):
        sleep(1)
        print i
        
def parent():
    
    pid = os.fork()
    if pid == 0:
        child()
    
    exit()

parent()