#!/usr/bin/python

__all__ = "ErrorBase"

from inspect import stack, getmembers
from sys import exc_info, exit
from linecache import getline
from os import path
import traceback
 
class ErrorBase(Exception):
    pass

class InputError(Exception):
    '''
    Exception raised for errors in the input

    Attributes:
        expr - input argument
        msg - explanation of the error
        sev -
    '''
    def __init__(self, expr, sev, msg):
        self.expr = expr
        self.msg = msg
        self.sev = sev
    
def process_input(input):

    try:
        if int(input): pass
    except:
        raise InputError(input,"FATAL","needs to be an int")
   
    if (input >= 0 and input <= 10):
        raise ValueError(input, "WARN","needs to be >= 0 and <= 10")

    return(input)

def process_input_raw(input):
    try:
        int(input)
    except ValueError,e:
        print e
        
    return(input)
    
if __name__ == '__main__':

    while 1:
        try:
            usrInput = raw_input( "\nPlease enter the magic number: " )
            process_input(usrInput)
        except InputError, e:
            #print "e.msg",e.msg
            #print "e.message", e.message
            #print dir(e)
            #print traceback.print_exception(InputError)
            #print "\n\nprint_exc\n",traceback.print_exc()
            #print "\n\nextract_stack\n",traceback.extract_stack()
            #print "\n\nprint_last\n",traceback.print_last()
            error_type,error_value,tb = exc_info()
            #print type(exc_info())
            #print "\n\nexc_info\n",exc_info()
            #print "Error type:",error_type
            print "Error type:",error_type
            
            print "Traceback",tb
            while tb.tb_next:
                tb = tb.tb_next
            stack = []
            f = tb.tb_frame
            while f:
                stack.append(f)
                f = f.f_back
            stack.reverse()
            for frame in stack:
                print "\n\nFrame: %s" % (frame.f_code.co_name)
                print "File:  %s" % (path.split(frame.f_code.co_filename)[1])
                print "Path:  %s" % (frame.f_code.co_filename)
                print "Line#: %s" % (frame.f_lineno)
                print "Code:  %s" % getline(path.split(frame.f_code.co_filename)[1], frame.f_lineno)

                for key,value in frame.f_locals.items():
                    print "\t%20s= " % key,
                    try:
                        print value
                    except:
                        print "error printing value"
                                
                #print "Tb Line no.",str(tb.tb_lineno)
                #print "Tb Last i.",str(tb.tb_lasti)
                #print "Tb Next.",str(tb.tb_next)
                #print "Tb Frame",tb.tb_frame
                #print "dir(tb.tb_frame)",dir(tb.tb_frame)
                #print "Frame code",tb.tb_frame.f_code
            
                #print "Value.args",error_value.args
                #print "dir(tb)",dir(tb)
                #print traceback.format_exception(error_type,error_value,tb)
            all_stack_dummy = traceback.extract_stack()
            all_stack = traceback.extract_stack()
            print all_stack
            print "actual call:%s" % (all_stack[-1:][0][3])


            ***** need to read about what actually are tracebacks, stacks and frames
            
            #*** how do i print out other stuff about the error, traceback/stack etc**
            #*** should what to do be stored in the error object ***
            #*** how can i get to the code behind TypeError i.e. ***
            #raise TypeError
        else:
            raise Exception
        #exit()

