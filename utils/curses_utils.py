from sys import path
path.append("/home/burtnolej/Development/pythonapps3/utils/")
from misc_utils import Singleton
from curses import wrapper, newwin, A_REVERSE, A_NORMAL, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, COLS, mousemask
from collections import OrderedDict
import time
import threading

lock = threading.Lock()
    
def _lock(func):
    def _tmp(*args, **kw):
        with lock:
            func(*args, **kw)
    return _tmp

class Window(threading.Thread):
#class Window(object):

    _debug = False
    _debug_win = None
    
    def __init__(self,wm,name,sy,sx,y,x,content=None,debug=False):
        '''
        args:
        sy = size of y axis (height)
        sx = size of x axis (width)
        y = begin y coord (origin)
        x = begin x coord (origin)
        focus = boolean, true to force the cursor to this win otherwise first win
        content is a list of any initial content you want to see
        '''
        assert isinstance(content,list) or content==None
        assert int(sy)

        threading.Thread.__init__(self)
                
        self._contents = []
        self._contents_top = None # index to content that represents  whats visible on the screen
        self._contents_bottom = None
        self._content_selection_idx = 0
        self._oy = 1
        self._ox = 1
        self._sy = sy -2 # (take off 2 for the borders)
        self._sx = sx -2 # (take off 2 for the borders)
       
        self._name = name
        self._win_ref = newwin(sy,sx,y,x)
        self.draw_name(y,x)
                
        self._win_ref.border()
        self._win_ref.keypad(1)
        
        self.set_focus_origin()
        self.refresh()

        if content != None:
            self._contents = content
            self.draw_content(0)
            self._contents_len = len(self._contents)
        if debug:
            Window._debug = True
            Window._debug_win = self

        wm.add_win(self) #register with the wm

    def run(self):
        while 1:
            time.sleep(1)


    def draw_name(self,y,x):
        win = newwin(3,self._sx+2,y-2,x) # add 2 back on for borders
        win.border()
        win.addstr(1,2,self._name)
        win.refresh()

    #def get_win(sy,sx,y,x):
    #    win = curses.newwin(3,self._sx+2,y-2,x) # add 2 back on for borders


    def set_focus_origin(self):
        '''
        to be overriden for subclass that want different behaviour
        ie list will want to change attribute to highight new focussed element
        '''
        self._win_ref.move(self._oy,self._ox)

    def set_focus_bottom(self):
        '''
        as set focus origin
        '''
        self._win_ref.move(self._oy+self._sy,self._ox+self._sx)


    def event_handler(self,event):
        '''
        to be over-ridden as specific to function of window
        '''
        pass

    def onclick_handler():
        pass

    def blank_content(self):
        for i in range(self._oy,self._sy+1):
                self.addstr_yx(i,self._ox,"          ")
                self.move(i,self._ox)
        self.set_focus_origin()

    def draw_content(self,start,cursor_bottom=False):
        '''
        args:
        start is where in _contents we should draw from if start == 0 then its the start
        cursor_bottom is to force focus element to be the bottom not the top (default)
        '''
        self.set_focus_origin() # make sure at origin
        self.blank_content()
        
        end = start+self._sy
        if end > len(self._contents):
            end = len(self._contents)
            
        for i in range(start,end):
                self.addstr_yx(self._y,self._ox,self._contents[i])
                self.move(self._y+1,self._ox)
                
        ###
        ### need to eliminate local _y _x and find a way
        ### to always call getxy
        ###                   
        self._contents_bottom = start+ self._sy
        if cursor_bottom:
                self.set_focus_bottom()
                
        else:
                self.set_focus_origin()


    def addstr_yx(self,y,x,text,attr=None):
        with lock:
            self._win_ref.addstr(y,x,text) # rewrite with new attr


    def addstr(self,text):
        self.addstr_yx(self._y,self._x,text) # rewrite with new attr
        
    @property
    def _y(self):
        y,_ = self._win_ref.getyx()
        return(y) 

    @property
    def _x(self):
        _,x = self._win_ref.getyx()
        return(x)

    @property
    def _content_selection(self):
        return(self._contents[self._content_selection_idx])

    def get_yx(self):
        return(self._y,self._x)


    def delch(self,y,x):
        self._win_ref.delch(y,x)

    def move(self,y,x):
        with lock:
            self._win_ref.move(y,x)

    def refresh(self):
        #with lock:
        self._win_ref.refresh()

    def getch(self):
        win_ref = self._win_ref
        return(win_ref.getch())

    def addstr_no_cursor(self,attr,y,x,width,win=None):
        '''
        write a string to a specific without moving the cursor
        useful for debug statements
        args:
        width is the number of chars expected so can blank out before each write
        win is set if the attr to print id not of parent object
        '''
        if win:
            text = str(getattr(win,attr))
            text = text.rjust(width+ 1) + " " + attr.ljust(30) + win._name
        else:
            text = str(getattr(self,attr))
            text = text.rjust(width+ 1) + " " + attr.ljust(30) + self._name
        
        cy, cx = self.get_yx() # get current pos of cursor
        self.addstr_yx(y,x,"".ljust(width))
        self.addstr_yx(y,x,text)
        self.move(cy,cx)


class ListBox(Window):

    def __init__(self,*args):
        super(ListBox,self).__init__(*args)
        
        if super(ListBox,self)._debug:
        #    super(ListBox,self)._debug_win.register("_content_selection_idx",8,self)            
        #    super(ListBox,self)._debug_win.register("_content_selection_idx",8,self)
            super(ListBox,self)._debug_win.register("_y",8,self)
            super(ListBox,self)._debug_win.register("_sy",8,self)
        #    super(ListBox,self)._debug_win.register("_content_selection",8,self)
        
        self.refresh()
        
    
    def set_row_attribute(self,screen,y,x,attr):
        text_at_row = screen.instr(y,1,self._sx) # get row text
        screen.addstr(y,1,text_at_row,attr) # rewrite with new attr
        screen.move(y,x) # return cursor to origin

    def set_focus_origin(self):
        '''
        to be overriden for subclass that want different behaviour
        ie list will want to change attribute to highight new focussed element
        '''
        self._win_ref.move(self._oy,self._ox)
        self.set_row_attribute(self._win_ref,self._oy,self._ox,A_REVERSE)

    def set_focus_bottom(self):
        '''
        as set focus origin
        '''
        self._win_ref.move(self._oy+self._sy-1,self._ox+self._sx)
        self.set_row_attribute(self._win_ref,self._oy+self._sy-1,self._ox,A_REVERSE)

    def event_handler(self,event):
        
        y, x = self.get_yx() # get current pos of cursor
        
        if event == KEY_LEFT:
            if x>0:
                self._win_ref.move(y,x-1)
        elif event == KEY_RIGHT:
            if x<COLS-1:
                self._win_ref.move(y,x+1)
        elif event == KEY_UP:
            if self._content_selection_idx == 0: # first element in content list
                self.set_row_attribute(self._win_ref,y,x,A_NORMAL)
                new_top = (len(self._contents)//self._sy) * self._sy # calculate top of last list content ( that contains the last element)
                self._content_selection_idx = new_top
                self.draw_content(new_top)
            elif y == 1: # highest visible element
                self.set_row_attribute(self._win_ref,y,x,A_NORMAL)
                self.draw_content(self._content_selection_idx - self._sy,True)
                self._content_selection_idx -= 1 
            else:  # just move
                self.set_row_attribute(self._win_ref,y,x,A_NORMAL)
                self.set_row_attribute(self._win_ref,y-1,x,A_REVERSE)
                self._content_selection_idx -= 1
        elif event == KEY_DOWN:
            if self._content_selection_idx == len(self._contents)-1: # last element in content list
                self.set_row_attribute(self._win_ref,y,x,A_NORMAL)
                self._content_selection_idx = 0
                self.draw_content(0)
            elif y == self._sy: # lowest visible element
                self.set_row_attribute(self._win_ref,y,x,A_NORMAL)
                self._content_selection_idx = self._contents_bottom
                self.draw_content(self._content_selection_idx)
            else: # just move 
                self.set_row_attribute(self._win_ref,y,x,A_NORMAL)
                self.set_row_attribute(self._win_ref,y+1,x,A_REVERSE)
                self._content_selection_idx += 1
        elif event == 4: # CTRL-d
            self.set_row_attribute(self._win_ref,y,x,A_NORMAL)
            if self._contents_bottom -1 < len(self._contents):
                self._content_selection_idx = self._contents_bottom - 1
                self.draw_content(self._content_selection_idx-1)
            else:
                self._content_selection_idx = 0
                self.draw_content(self._content_selection_idx)
        elif event == 21: # CTRL-u
            pass
        elif event == 10:
            text_at_row = self._win_ref.instr(y,0,COLS) # get string at xy
        else:
            return(False)
        
        return(True)

class DebugBox(Window):

    def __init__(self,*args):
        super(DebugBox,self).__init__(*args)
        self.attr_list = OrderedDict()
        self.next_free = 1


    def register(self,text,width,win):
        '''
        store details of watch in an ordered dict of tuples
        dict1{"attr"+win} = attr, win_ref, width, index
        index = order on the screen (y coord)
        '''
        if not self.attr_list.has_key(text + str(win)):
            self.attr_list.__setitem__(text + str(win),(text,win,width,self.next_free))
            self.next_free += 1
        else:
            pass
            #raise Exception # nothing should try to register twice

    def run(self):

        while 1:
            for key in self.attr_list.keys():
                text,win,width,index = self.attr_list.__getitem__(key)
            
                self.addstr_no_cursor(text,index,1,width,win)
            time.sleep(1)
            self.refresh()
            
class TextBox(Window):

    def __init__(self,*args):
        super(TextBox,self).__init__(*args)
    
        if super(TextBox,self)._debug:
            super(TextBox,self)._debug_win.register("_y",8,self)
            super(TextBox,self)._debug_win.register("_x",8,self)


    def run(self):
        while 1:
            #self.addstr_yx(1,1,get_time_hms())
            self.addstr_yx(1,1,"the time")
            #with lock:
            self.refresh()
            time.sleep(1)
            #self.addstr('x')
            #pass
        
class EntryBox(Window):

    def __init__(self,*args):
        super(EntryBox,self).__init__(*args)
    
        if super(EntryBox,self)._debug:
            super(EntryBox,self)._debug_win.register("_y",8,self)
            super(EntryBox,self)._debug_win.register("_x",8,self)

    def event_handler(self,event):
        if event == 263: # delete
            if self._x >0:
                self.delch(self._y,self._x-1)
        elif event == KEY_LEFT:
            if self._x>0:
                self.move(self._y,self._x-1)
        elif event == KEY_RIGHT:
            if self._x<COLS-1:
                self.move(self._y,self._x+1)
        elif event == KEY_UP:
            pass
        elif event == KEY_DOWN:
            pass
        elif event == 10:
            pass
        else:
            self.addstr(chr(event))

    def run(self):
        while 1:
            time.sleep(1)
    
class WindowManager():
    __metaclass__ = Singleton
    '''
    rudimentary window manager
    '''
    def __init__(self):
        '''
        '''
        self._wins = [] # refs to all the windows init'd
        self._focus = 0 # index of _wins containing current focus

    def add_win(self,win_ref,focus=False):
        '''
        add a win to be handled by the manager
        '''
        self._wins.append(win_ref)
        if focus:
            self_focus = len(self._wins)-1

    def get_win_ref(self,index=None):
        '''
        get ref of win in focus or ref of win index
        '''
        assert len(self._wins) > 0
         
        if index==None:
            return(self._wins[self._focus])
        else:
            self._focus = index
        return(self._wins[index])

    def get_next_win_ref(self):
        if (self._focus + 1) < len(self._wins): # if one more left
            self._focus += 1
        else:
            self._focus = 0
        return(self.get_win_ref(self._focus))

    def event_handler(self,event):
        '''
        needs to be the first event handler always called and then
        throw to the window in focus if keypress not handled here
        '''        
        if event == 9: # tab is the key to switch window focus
            focus_win = self.get_next_win_ref()
            focus_win.refresh
            return(True)
        elif event == ord("q"):
            exit()
        return(False)

    def mainloop(self):
        while True:
            focus_win = self.get_win_ref()
            focus_win.refresh()
            event = focus_win.getch()
            if not focus_win.event_handler(event):
                self.event_handler(event)

def file2list(filename):
    l=[]
    fh = open(filename, 'r+')
    return [line.rstrip() for line in fh]
 
    
def main(screen):

    l = file2list("./list.txt")
    
    screen.keypad(1)
    mousemask(1)

    wm = WindowManager()
    db = DebugBox(wm,"db1",10,50,26,5,None,True)
    db.daemon = True
    db.start()
    db.name = "db1"
    
    #lb = ListBox.listcontent(wm,"lb1",15,50,8,5,l)
    lb = ListBox(wm,"lb1",15,50,8,5,l)
    lb.daemon = True
    lb.start()
    lb.name = "lb1"
    
    #lb2 = ListBox.listcontent(wm,"lb2",15,50,8,60,l)
    lb2 = ListBox(wm,"lb2",15,50,8,60,l)
    lb2.daemon = True
    lb2.start()
    lb2.name = "lb2"

    eb = EntryBox(wm,"eb1",3,50,2,5,None)
    eb.daemon = True
    eb.start()
    eb.name = "eb1"
    
    tb = TextBox(wm,"tb1",3,50,39,5,None)
    tb.daemon = True
    tb.start()
    tb.name = "tb1"
    
    wm.mainloop()

if __name__ == '__main__':
    try:
        wrapper(main)
    except KeyboardInterrupt:
        print "Got KeyboardInterrupt exception. Exiting..."
        exit()

    
