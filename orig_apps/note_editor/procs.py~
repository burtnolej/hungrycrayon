#!/usr/bin/python

from sys import path, argv
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, db_query_dec
from inspect import getmembers, getdoc
#from proc_util import QryStr, q_cn, q_tn, list_procs

class NotesDB(Database):
    pass

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

q=QryStr(NotesDB,"~/Downloads/gadflyZip/gadfly/scripts/",'use')

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


@db_query_dec(q.db,q.loc,q.perm)
def q_db(*arg):
    '''
    select title,tag_name from db
    '''
    assert len(arg) == 2
    q.add("select n.title,")
    q.add("       t.name")
    q.add("from   notes as n,")
    q.add("       tags as t,")
    q.add("       notetags as nt")
    q.add("where  n.id = nt.noteid")
    q.add("and    nt.tagid = t.id")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_d(*arg):
    '''
    select distinct dates where arg=create|modify
    '''
    assert len(arg) == 1
    q.add("select distinct date")
    q.add("from   dateconversions")
    q.add("where  datatype = 'date'")
    q.add("and    actiontype = '" + arg[0] + "'")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_dc(*arg):
    '''
    from dateconversions where arg='dd/mm/yyyy'
    '''
    assert len(arg) == 3
    q.add("select secs")
    q.add("from   dateconversions")
    q.add("where date = '" + arg[2] + "'") 
    return(q.result)
    


if __name__ == '__main__':
    # remove first 2 mandatory args pass in optional args so that
    # procs can be called directly from other modules
    base_args = argv[:2]
    opt_args = argv[2:]
    if len(base_args) == 1:
        list_procs()
        exit()

    for rec in locals()[argv[1]](*opt_args):
        print rec

    '''
    this is how to call the procs from a 

    for rec in procs.q_d('create'):
        print rec
    '''

