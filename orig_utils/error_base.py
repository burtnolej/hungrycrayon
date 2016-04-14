#!/usr/bin/python

__all__ = "ErrorBase"

import misc_util
from inspect import stack
from sys import exc_info
 
class ExceptionBase(Exception):

    '''
    store in here a count of the eceptions thrown
    keep the tracebacks here
    have all exceptions subclass this
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    def _print(self):
        misc_util.print_object(self.__class__)

class ExceptionCollection(dict):
    
class InputCharError(ErrorBase):
    error_msg = "Input character is invalid"
