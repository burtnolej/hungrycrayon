#!/usr/bin/python

__all__ = "ErrorBase"

import misc_util
from table_print import SimpleTable,Table
from stack_util import get_inner_frames, get_outer_frames,FrameRecord,clear_list, tmp_print, get_exception_info

from inspect import stack
from sys import exc_info
from os import path
from linecache import getline
from inspect import getmembers,getinnerframes

class Notification(Exception):
    _store = {}

    @staticmethod
    def print_summary(attr=None):
        '''
        summarise the exceptions/notifications caught
        and then print out details for each
        arg : attr string - name a specific attr in the frame that
        needs to be printed out
        '''
        SimpleTable(Notification,0,2,1).deep_print()
        
        for et in Notification._store:
            for inst in Notification._store[et]['instances']:
                SimpleTable(inst).printout()
                if attr: Table(inst.locals[attr]).printout()
                
        
    @staticmethod
    def myraise(exc=None):
        try:
            raise exc
        finally:
            exc._enrich()

    def _add(self,fr):
        fr.error_type = self.__class__.__name__
        fr.error_value = self.message
        if Notification._store.has_key(fr.error_type):
            Notification._store[fr.error_type]['count'] += 1
        else:
            Notification._store[fr.error_type] = {}
            Notification._store[fr.error_type]['count'] = 1
            Notification._store[fr.error_type]['instances'] = []

        Notification._store[fr.error_type]['instances'].append(fr)

    add = staticmethod(_add)

    def _enrich(self):
        get_outer_frames() # loads FrameRecord with frames
        self._add(FrameRecord._list[3]) #3 fr offset betw raise/myraise
        clear_list()

    @staticmethod
    def enrich(exc):
        '''
        retrieve inner frames to get frame where exception was raises
        this is an offset of 1.
        get_inner_frames loads FrameRecord with frames
        exc : class instance - exception
        '''
        get_inner_frames()
        no_fr = len(FrameRecord._list)
        Notification.add(exc,FrameRecord._list[no_fr-1])
        clear_list()


class MyException(Notification):
    def __init__(self,*arg,**kwargs):
        super(MyException,self).__init__(*arg, **kwargs)
        self._sev = 1

class MyAlert(Notification):
    def __init__(self,*arg,**kwargs):
        super(MyAlert,self).__init__(*arg, **kwargs)
        self._sev = 2
    pass

class MyComment(Notification):
    def __init__(self,*arg,**kwargs):
        super(MyAlert,self).__init__(*arg, **kwargs)
        self._sev = 3
    pass
    
if __name__ == '__main__':

    def afunc():
        _alocal = {}
        _blocal = 'dsadsd'

        Notification.myraise(MyException('my exception'))

    def efunc():
        _efunc = 'eeeeeee'
        Notification.myraise(MyException('my deep exception'))
        
    def dfunc():
        _dfunc = 'ddddddd'
        efunc()
        
    def bfunc():
        _alocal = {}
        _blocal = 'dsadsd'
        Notification.myraise(MyAlert('my alert'))

    def cfunc():
        _alocal = {}
        _clocal = 'cccccc'
        raise ValueError
        
    #try:
    #    afunc()
    #except MyException,e:
    #    pass
        
    #try:
    #    dfunc()
    #except MyAlert,e:
    #    pass
    #except MyException,e:
    #    pass
        
    try:
        cfunc()
    except MyException,e:
        pass
    except:
        e = get_exception_info()
        Notification.enrich(e['value'])
        
    Notification.print_summary()
