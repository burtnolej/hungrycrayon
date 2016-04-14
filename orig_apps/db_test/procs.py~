#!/usr/bin/python

from sys import path, argv
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, db_query_dec
from inspect import getmembers, getdoc

class Finance(Database):
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

q=QryStr(Finance,"~/Downloads/gadflyZip/gadfly/scripts/",'use')

def list_procs():
    prefix = {"q_":"queries:","d_":"drops:"}
    for p,d in prefix.iteritems() :
        print d
        print "".join([" " + key.ljust(20) + str(getdoc(value)) + "\n" for key,value in globals().iteritems() if str(key).startswith(p)])

@db_query_dec(q.db,q.loc,q.perm)
def q_ct_summary(*arg):
    '''
    select from counterpartytypes
    '''
    assert len(arg) == 2
    q.add("select offscreen,")
    q.add("       c.name,")
    q.add("       keywords,")
    q.add("       keywordssnippet")
    q.add("from   counterpartytypes,")
    q.add("       counterpartys as c")
    q.add("where  c.id = cpy_id")
    q.add("and    result_count=2")
    #q.add("order by cpy_id"
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_ct_summary2(*arg):
    q.add("select name")
    q.add("from   counterpartys")
    q.add("order by name")
    return(q.result)
    
@db_query_dec(q.db,q.loc,q.perm)
def d_ct(*arg):
    '''
    drop counterpartytypes
    '''
    assert len(arg) == 2
    q.add("drop   table counterpartytypes")
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
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_c(*arg):
    assert len(arg) == 2
    q.add("select count(*)")
    q.add("from   counterpartys")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_ct(*arg):
    assert len(arg) == 2
    q.add("select count(*)")
    q.add("from   counterpartytypes")
    return(q.result)

@db_query_dec(q.db,q.loc,q.perm)
def q_t_btw(*arg):
    '''
    from transations > 'dd/mm/yyyy' & < 'dd/mm/yyyy'
    '''
    assert len(arg) == 4
    q.add("select tran_date,")
    q.add("       tran_secs,")
    q.add("       sum(debit_amt),")
    q.add("       count(*)")
    q.add("from   transactions")
    q.add("where  tran_secs > (select   secs")
    q.add("                    from     dateconversions")
    q.add("                    where    date = '" + arg[2] + "')")
    q.add("and    tran_secs < (select   secs")
    q.add("                    from     dateconversions")
    q.add("                    where    date = '" + arg[3] + "')")
    q.add("group  by tran_date,tran_secs")
    q.add("order  by tran_secs")
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
def q_dc(*arg):
    '''
    from dateconversions where arg='dd/mm/yyyy'
    '''
    assert len(arg) == 3
    q.add("select secs")
    q.add("from   dateconversions")
    q.add("where date = '" + arg[2] + "'") 
    return(q.result)

if len(argv) == 1:
    list_procs()
    exit()

exec argv[1] + "(*argv)"

    
