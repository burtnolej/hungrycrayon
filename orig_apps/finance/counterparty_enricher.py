#!/usr/bin/python

from sys import path, argv, stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Logger
from counterparty import Counterpartys, Counterparty
from transaction import Transactions, Transaction
from transaction_type import TransactionTypes, TransactionType
#from counterparty_type import CounterpartyTypes, CounterpartyType
from collections import OrderedDict
from db_util import Database, DatabaseTable, DatabaseRecord
from url_util import *
from table_print import SimpleTable
from error_util import Notification
from thread_util import MyThread, active_threads, active_thread_count
from multiprocessing.pool import ThreadPool
import threading
from time import sleep
import subprocess
import re
import copy

l = Logger("/private/tmp/log.txt")

class YellDataItems(URLDataItems):
    def __init__(self,cpy,loc):
        self.get_url(self._gen_url(cpy,loc))
        # modify _doc
        self.doc = self.doc.split("<div class=\"parentListing\"")
        
    def _gen_url(self,cpy,loc):
        url = "http://www.yell.com/ucs/UcsSearchAction.do?keywords="
        url += cpy
        url += "&location="
        url += loc
        url += "&scrambleSeed=58471740&searchType=&M=&bandedclarifyResults=&ssm=1"
        return(url)

class Finance(Database):
    pass

class CounterpartyTypes(DatabaseTable):
    def add(self,**kwargs):
        tmp_kwargs = copy.deepcopy(kwargs) # avoid writing into kwargs being read
        for k,v in tmp_kwargs.iteritems():
            new_attr_name = '_db_'+"".join(k.split()).lower()
            kwargs.__setitem__(new_attr_name,v)
            kwargs.__delitem__(k)
        
        dr = DatabaseRecord(**kwargs)
        dr._db_id = dr._id # make id a db atribute
        
        self[dr._db_id] = dr

d = OrderedDict({'offscreen':[('span','class=','')],
                     'streetAddress':[('span','itemprop=','')],
                     'addressLocality':[('span','itemprop=',''),
                                        ('strong','','')],
                     'addressLocality':[('span','itemprop=',''),
                                        ('strong','','')],

                     'postalCode':[('span','itemprop=','')],
                     'keywords':[('div','class=',''),
                                 ('p','',''),
                                 ('strong','','')],
                     'keywords snippet':[('div','class=',''),
                                 ('p','',''),
                                 ('a','','[^>]*')]})

finance = Finance("~/Downloads/gadflyZip/gadfly/scripts/",'use')

ctc = finance.table(CounterpartyTypes())

qry_str  = "select id,name "
qry_str += "from   counterpartys "
qry_str += "order by name"

finance.execute(qry_str)

threads = []
threadLock = threading.Lock()
pool = ThreadPool(processes=1000)

def process_cpy(cpy,cpy_id):
    try:
        yd = YellDataItems(cpy,'London')
        yd.scrape(d,cpy)

        for res in yd:
            res.__setitem__('cpy_id',cpy_id)
            ctc.add(**res)
            
    except URLSearchStringAlert:
        pass
    except URLFindallLenAlert:
        pass
    except URLFindall0LenAlert:
        pass

thread1 = None
#for cpy_id,cpy in finance.fetchall_like('name','WAITROSE'):
#for cpy_id,cpy in finance.fetchall_like('name','^W.*'):

for cpy_id,cpy in finance.fetchall():
    thread1 = MyThread(cpy,process_cpy,cpy=cpy,cpy_id=cpy_id)
    thread1.start()

    #l.tmp_stdout.write('\b')
    wstr="\r" + cpy[0:1] + " " + str(active_thread_count())
    l.tmp_stdout.write(wstr)
    l.tmp_stdout.flush()
    sleep(0.05)

while atc_check(l.tmp_stdout):
    sleep(0.1)

#sleep(5)

if len(ctc) > 0:
    finance.commit()
    ctc.empty()

del l
    
finance.close()

SimpleTable(Notification,0,2,1).deep_print()
#SimpleTable(Notification,0,5,4).deep_print()


