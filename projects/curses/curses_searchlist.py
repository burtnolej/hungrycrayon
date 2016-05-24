from sys import path
path.append("/home/burtnolej/Development/pythonapps3/utils/")
import curses_utils

def main(screen):

    l = file2list("./list.txt")
    
    screen.keypad(1)
    curses_utils.mousemask(1)
    
    wm = WindowManager()
    
    lb = ListBox(wm,"lb1",15,50,8,5,l)
    lb.daemon = True
    lb.start()
    lb.name = "lb1"
    
    wm.mainloop()

if __name__ == '__main__':
    try:
        curses_utils.wrapper(main)
    except KeyboardInterrupt:
        print "Got KeyboardInterrupt exception. Exiting..."
        exit()