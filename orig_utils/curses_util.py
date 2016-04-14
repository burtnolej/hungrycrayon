#!/usr/bin/python

import sys
import curses
import inspect
from misc_util import switch,Logger,in_method_log

# needs to be sorted
list = ['nancy',
        'quinton',
        'jon',
        'nanval',
        'granpops']

Y_COUNT=20
X_COUNT=0

Y_RESULTS=22
X_RESULTS=0

class CoordTypeError(Exception):
    error_msg = "coord type must be in 'x,y'"
class ScreenCoordValueError(Exception):
    error_msg = "value must be >0 and < terminal width and height"


class CursesPane():
    # base curses pane

    def __init__(self,screen):

        curses.setupterm()
        self._num_colors = curses.tigetnum("colors")        
        self._screen = screen
        self.max_y,self.max_x = self._screen.getmaxyx()
        self._widget_list = ()
        self.cursor_x = 0
        self.cursor_y = 0 # where the cursor is on the screen
        self.input_str = ""
        if self._num_colors != -1:
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
                curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

    @in_method_log()
    def set_cursor_coord(self,coord,value):
        '''
        set the value of member attr cursor_x or cursor_y
        coord needs to be char in 'x,y'; value: value int within term range

        '''
        if coord != 'x' and coord != 'y':
            raise CoordTypeError
        if coord == 'x' and value < 0 and value > self.max_x:
            raise ScreenCoordValueError
        if coord == 'y' and value < 0 and value > self.max_y:
            raise ScreenCoordValueError
        else:
            attr = "cursor_"+coord
            setattr(self,attr,value)
            return(True)

    @in_method_log   
    def set_cursor_coord_offset(self,coord,offset):
        attr = "cursor_"+coord
        tmp_value = self.get_cursor_coord(coord) + offset
        setattr(self,attr,tmp_value)
        return(tmp_value)

    @in_method_log   
    def get_cursor_coord(self,coord):
        attr = "cursor_"+coord
        return(getattr(self,attr))

    @in_method_log   
    def get_cursor_coord_xy(self):
        return(self.get_cursor_coord('x'),self.get_cursor_coord('y'))
        

    @in_method_log   
    def move_cursor_on_screen_abs(self,x=None,y=None):
        if x==None:
            self._screen.move(self.get_cursor_coord_xy)
        else:
            self._screen.move(x,y)
            self.set_cursor_coord('x',x)
            self.set_cursor_coord('y',y)

    @in_method_log        
    def move_cursor_on_screen_offset(self,x_offset,y_offset): 
        x_tmp = self.get_cursor_coord('x') + x_offset
        y_tmp = self.get_cursor_coord('y') + y_offset
  
        self._screen.move(y_tmp,x_tmp)
        
        self.set_cursor_coord('x',x_tmp)
        self.set_cursor_coord('y',y_tmp)
        return(y_tmp,x_tmp)

        
    @in_method_log
    def write_char_to_screen(self,char,color_pair_id,supress_increment,x=None,y=None):
        '''
        write 'char' to the screen at position x,y if specified
        or write 'char' to the screen at the current cursor position
        x_cursor,y_cursor
        set supress_increment to not None if deleting a char (writing a blank)
        '''
        if self._num_colors != -1:
            color_pair = curses.color_pair(color_pair_id)
        else:
            color_pair = 1
        
        if (x != None): # do not use current cursor posn
            self.move_cursor_on_screen_abs(x,y)
        
        self._screen.addstr(str(chr(char)),color_pair)

        if supress_increment == False: # do not supress cursor increment
            self.set_cursor_coord_offset('x',1)
        else:
            self.move_cursor_on_screen_abs(x,y)
            
        return(self.get_cursor_coord_xy())

    @in_method_log
    def write_blank_line_to_screen(self):
        self.move_cursor_abs(0,0)
        self._screen.hline(self.get_cursor_coord('y'), 0, " ", self.max_x)
        
    @in_method_log
    def get_char(self):
        return(self._screen.getch())


    @in_method_log
    def set_input_str(self,type,new_string=None):
        '''
        update the line on the screen that is being used as input
        args :
        type - indicates the type of effect needed NEW=replace existing string with new_string CLEAR=set to BLANK str DEL=delete the last char, ADD=add new_string to existing visible string
        new_string - optional contains any new string to be drawn

        return:
        the new value of the input str which is equal to whats shown on the screen
        '''
        for case in switch(type):
            if case('NEW'):
                self.input_str = new_string
                break
            if case('CLEAR'):
                self.input_str = ''
            if case('DEL'):
                self.input_str = self.get_input_str()[0:len(self.get_input_str())-1]
                break
            if case('ADD'):
                self.input_str += chr(new_string)
                break
        return(self.input_str)

    def get_input_str(self):
        return(self.input_str)

def main(screen):
    
    cp = CursesPane(screen) # init curses screen
    
    while 1:

        c = cp.get_char() # get the latest char input
        
        for case in switch(c):
            if case(ord('Q')): 
                return  # Exit the while() on a q
            if case(curses.KEY_LEFT): # reset the line to blank
                cp.set_input_str('CLEAR') # reset the input line
                cp.write_blank_line_to_screen()
                break
            if case(curses.KEY_BACKSPACE): # delete last char
                cp.set_input_str('DEL')
                cp.move_cursor_on_screen_offset(-1,0)
                cp.write_char_to_screen(ord(' '),1,True)
                break
            if case(curses.KEY_ENTER):
                cp.move_cursor_on_screen_offset(0,1)
                break
            if case(ord('A')): #'fn key'
                cp.set_cursor_coord('z',4)
                break
            else :
                cp.set_input_str('ADD',c)
                cp.write_char_to_screen(c,1,False) # print the char to the screen

if __name__ == '__main__':
    l = Logger("/private/tmp/log.txt",True)
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print "Got KeyboardInterrupt exception. Exiting..."
        exit()
    del l

