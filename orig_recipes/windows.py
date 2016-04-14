#!/usr/bin/python

import curses

class Win():
    _wins = []
    _focus = 0
    
    def __init__(self,parent,sy,sx,y,x,focus=False):
        '''
        args:
        sy = size of y axis (height)
        sx = size of x axis (width)
        y = begin y coord (origin)
        x = begin x coord (origin)
        focus = boolean, true to force the cursor to this win otherwise first win
        '''
        self._win_ref = curses.newwin(sy,sx,y,x)
        self._win_ref.border()
        self._win_ref.keypad(1)
        Win._wins.append(self._win_ref)
        if focus:
            Win._focus = len(Win._wins)-1

def get_win_ref(index=None):
    if index==None:
        return(Win._wins[Win._focus])
    else:
        Win._focus = index
        return(Win._wins[index])

def get_next_win_ref():
    if (Win._focus + 1) < len(Win._wins): # if one more left
        Win._focus += 1
    else:
        Win._focus = 0
    return(get_win_ref(Win._focus))
        
        
def populate_list(screen,filename):
    fh = open(filename, 'r+')
    l = []
    [l.append(line) for line in fh]
    return(l)

def set_row_attribute(screen,y,x,attr):
    text_at_row = screen.instr(y,0,curses.COLS-2) # get row text
    screen.addstr(y,0,text_at_row,attr) # rewrite with new attr
    screen.move(y,x) # return cursor to origin

def init_win(screen):
    '''
    draw wins
    return ref to win in focus
    '''
    Win(screen,30,30,0,0)
    Win(screen,30,30,0,32)
    Win(screen,5,5,0,64)
    return(get_win_ref())

def main(screen):

    curses.mousemask(1)
    win = init_win(screen)
    
    while True:
        win.refresh()
                                             
        event = win.getch()
        y, x = win.getyx() # get current pos of cursor
               
        if event == ord("q"): break
        elif event == 9: # tab
                win = get_next_win_ref()
        elif event == curses.KEY_LEFT:
                if x>0:
                        win.move(y,x-1)
        elif event == curses.KEY_RIGHT:
                if x<curses.COLS-1:
                        win.move(y,x+1)
        elif event == curses.KEY_UP:
                if y>0:
                        set_row_attribute(win,y,x,curses.A_NORMAL)
                        set_row_attribute(win,y-1,x,curses.A_REVERSE)
        elif event == curses.KEY_DOWN:
                if y<curses.LINES-2:
                        set_row_attribute(win,y,x,curses.A_NORMAL)
                        set_row_attribute(win,y+1,x,curses.A_REVERSE)
        elif event == 10:
                text_at_row = win.instr(y,0,curses.COLS) # get string at xy
                win.addstr(curses.LINES-2,0,text_at_row,curses.A_BLINK)
                
                win.move(y,x)
        else:
                win.addstr(chr(event),1)
        

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print "Got KeyboardInterrupt exception. Exiting..."
        exit()
