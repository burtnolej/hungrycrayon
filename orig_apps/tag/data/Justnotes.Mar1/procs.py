#!/usr/bin/python

from sys import path, argv
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, db_query_dec
from misc_util import datetime_to_secs,str_fmt_to_datetime
from inspect import getmembers, getdoc
from datetime import datetime

class TagDB(Database):
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

    def pprint(self):
        print 'value',self.value
        print 'db',self.db
        print 'loc',self.loc
        print 'perm',self.perm

q=QryStr(TagDB,"~/gadfly/scripts/",'use')

def list_procs():
    prefix = {"q_":"queries:","d_":"drops:"}
    for p,d in prefix.iteritems() :
        print d
        print "".join([" " + key.ljust(20) + str(getdoc(value)) + "\n" for key,value in globals().iteritems() if str(key).startswith(p)])

@db_query_dec(q.db,q.loc,q.perm)
def q_p(*arg):
    q.add("select last_name")
    q.add("from   players")
    return(q.result)
    
@db_query_dec(q.db,q.loc,q.perm)
def q_tn(*arg):
    '''
    select from __table_names__
    '''
    assert len(arg) == 2
    q.add("select *")
    q.add("from   __table_names__")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_cn(*arg):
    '''
    select from __columns__
    '''
    assert len(arg) == 2
    q.add("select *")
    q.add("from   __columns__")
    #print q.result
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_f_dt(*arg):
    '''
    from files modified > '%d/%m/%y %H:%M:%S' & < '%d/%m/%y %H:%M:%S'
    '''
    assert len(arg) == 4

    fmt='%d/%m/%y %H:%M:%S'
    start_secs = datetime_to_secs(str_fmt_to_datetime(arg[2],fmt))
    end_secs = datetime_to_secs(str_fmt_to_datetime(arg[3],fmt))
    
    q.add("select *")
    q.add("from   Files")
    q.add("where  modify_secs > " + str(start_secs))
    q.add("and    modify_secs < " + str(end_secs))
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_t(*arg):
    '''
    from transations where arg='dd/mm/yyyy'
    '''
    assert len(arg) == 3
    q.add("select tran_date,")
    q.add("       count(*)")
    q.add("from   transactions")
    q.add("where  tran_date = '" + arg[2] + "' ") 
    q.add("group  by tran_date")
    q.add("order  by tran_date")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_tn(*arg):
    '''
    from tag where name = 'tag'
    '''
    assert len(arg) == 3
    q.add("select *")
    q.add("from   Tags")
    q.add("where name = '" + arg[2] + "'") 
    return(q.result)

if len(argv) == 1:
    list_procs()
    exit()

exec argv[1] + "(*argv)"
