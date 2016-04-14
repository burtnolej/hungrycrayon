#!/usr/bin/python

from sys import path,argv,exit
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, DatabaseTable, DatabaseRecord, db_query_dec

class QryStr(object):
    def __init__(self,db,loc,perm):
        self.value = ""
        self.db = db
        self.loc = loc
        self.perm = perm
    def add(self,text):
        self.value = self.value + text + " \n"

    @property
    def result(self):
        tmp_value = self.value
        self.value = ""
        return tmp_value

    @result.setter
    def result(self,value):
        self.value = value

@db_query_dec(q.db,q.loc,q.perm)
def q_cn(*arg):
    '''
    select from __columns__
    '''
    assert len(arg) == 0
    q.add("select *")
    q.add("from   __columns__")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_tn(*arg):
    '''
    select from __table_names__
    '''
    assert len(arg) == 0
    q.add("select *")
    q.add("from   __table_names__")
    return(q.result)

def list_procs():
    prefix = {"q_":"queries:","d_":"drops:"}
    for p,d in prefix.iteritems() :
        print d
        print "".join([" " + key.ljust(20) + str(getdoc(value)) + "\n" for key,value in globals().iteritems() if str(key).startswith(p)])

