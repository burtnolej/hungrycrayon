#!/usr/bin/python

from sys import path, argv
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, db_query_dec
from inspect import getmembers, getdoc
#from proc_util import QryStr, q_cn, q_tn, list_procs

class NotesDB(Database):
    pass

class QryStr(object):
    def __init__(self,db=None,loc=None,perm=None):
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
def q_db(*arg):
    '''
    select title,tag_name from db
    '''
    q.add("select n.title,")
    q.add("       t.name")
    q.add("from   notes as n,")
    q.add("       tags as t,")
    q.add("       notetags as nt")
    q.add("where  n.id = nt.noteid")
    q.add("and    nt.tagid = t.id")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_ncd(*arg):
    '''
    select distinct dates where arg=create|modify
    '''
    q.add("select distinct date")
    q.add("from   dateconversions")
    q.add("where  datatype = 'date'")
    if len(arg) == 1:
        q.add("and    actiontype = '" + arg[0] + "'")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_nt(*arg):
    '''
    select tags for given create date
    '''
    q.add("select t.name")
    q.add("from   dateconversions as dc,")
    q.add("       notes as n,")
    q.add("       tags as t,")
    q.add("       notetags as nt")
    if arg[0]: # if no predicate then its passed as None
        q.add("where  dc.date = '" + arg[0] + "'")
        q.add("and    dc.actiontype = 'create'")
        q.add("and    dc.datetype = 'date'")
        q.add("and    n.created_secs = dc.secs")
        q.add("and    nt.noteid = n.id")
        q.add("and    t.id = nt.tagid")

    return(q.result)
    
@db_query_dec(q.db,q.loc,q.perm)
def q_nti(*arg):
    '''
    select note titles for given tag name
    '''
    
    q.add("select n.title,")
    q.add("       n.id")
    q.add("from   notes as n,")
    q.add("       tags as t,")
    q.add("       notetags as nt")
    if len(arg) == 1:
        q.add("where  t.name = '" + arg[0] + "'")
        q.add("and    nt.tagid = t.id")
        q.add("and    n.id = nt.noteid")
        
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_nc(*arg):
    '''
    select note content for given note title
    '''    
    q.add("select content")
    q.add("from   notes")
    q.add("where  title = '" + arg[0] + "'")
        
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_dc(*arg):
    '''
    from dateconversions where arg='dd/mm/yyyy'
    '''
    q.add("select secs")
    q.add("from   dateconversions")
    q.add("where date = '" + arg[0] + "'") 
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def u_n_c(*arg):
    '''
    update note content given a title
    '''
    q.add("update notes")
    q.add("set    content='" + arg[0] + "'")
    q.add("where  title='" + arg[1] + "'")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def i_nt(*arg):
    '''
    insert a new tag for a note
    '''
    rec = ",".join("'" + a + "'" for a in arg)
    
    q.add("insert into notetags (id, noteid, tagid)")
    q.add("            values (" + rec + ")")

    print q.value
    return(q.result)

## need to create something in db_util that
## inserts rows into existing tables
## reuse the code from the note_loader

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

