#!/usr/bin/python

from sys import path, argv, stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import file2list, switch, Logger, datetime_to_secs,secs_to_datetime, date_to_secs
from counterparty import Counterpartys, Counterparty
from transaction import Transactions, Transaction
from transaction_type import TransactionTypes, TransactionType
from operator import mod
from collections import OrderedDict
from db_util import Database, DatabaseTable

import subprocess
import re

l = Logger("/private/tmp/log.txt")

coutts_trans = file2list(argv[1])

class Finance(Database):
    pass

class DateConversions(DatabaseTable):
    pass

finance = Finance("~/Downloads/gadflyZip/gadfly/scripts/","create")
cc = finance.table(Counterpartys())
tc = finance.table(Transactions())
ttc = finance.table(TransactionTypes())
dcc = finance.table(DateConversions())
#DatabaseTable(table_name = 'DateConversions'))

if coutts_trans[0].split(",")[0] == 'Sort code':
    coutts_trans.pop(0) # remove header

for record in coutts_trans:
    # find any , between " " like "fdfsdf,ddf"
    p = re.compile('["][^"]*["]|[^,]*')
    y = p.findall(record)
    # re creates empty strings so need to remove them and keep real one 
    x = [y[i] for i in range(0,len(y)-1) if y[i+1] == '']
    # now remove the , from within the strings
    record = ",".join(z.replace(",","") for z in x)
    
    fields = record.split(",")
    mangle = re.sub("\"","",fields[3])

    if fields[6] == '':
        debit_amt = float(fields[5])
        tran_amt = float(debit_amt)
        credit_amt = float(0.0)
    else:
        credit_amt = float(fields[6])
        tran_amt = float(credit_amt)
        debit_amt = float(0.0)
        
    try:
        cpy = cc.add(_mangle = mangle,
                     _tran_amt = tran_amt)

        if hasattr(cpy,'c_name') :
            cpy._db_name = cpy.c_name
            delattr(cpy,"c_name")

        cpy._db_id = cpy._id

        tt = ttc.add(_mangle = mangle,
                    _tran_amt = tran_amt)

        tt._db_id = tt._id

        date = fields[2]
        secs = date_to_secs(date)
        dcc.add(_db_date = date,
                _db_secs = secs)

        t = tc.add(_db_credit_amt = credit_amt,
                   _db_debit_amt  = debit_amt,
                   _cpy           = cpy,
                   _db_cpy_id     = cpy._id,
                   _tt            = tt,
                   _db_tt_id      = tt._id,
                   _db_tran_secs  = secs,
                   _db_tran_date  = date,
                   _db_balance    = fields[7])
        #t._db_id = tt._id
        
    except KeyboardInterrupt:
        pass
        
finance.commit()

del l

input_file_len = subprocess.check_output(['wc','-l',argv[1]]).split()[0]
out_str =  "input file : " + str(argv[1]) + "\n"
out_str += "input lines : " + input_file_len + "\n"

stdout.write(out_str)

qry_str =  "select cpy_id,sum(debit_amt) "
qry_str += "from transactions "
qry_str += "where debit_amt < -1000 "
qry_str += "group by cpy_id"
#finance.run_qry(qry_str)

qry_str =  "select c.name, sum(t.debit_amt) "
qry_str += "from transactions as t, counterpartys as c "
qry_str += "where t.debit_amt < -1000 "
qry_str += "and t.cpy_id = c.id "
qry_str += "group by c.name "
qry_str += "order by 2"
#finance.run_qry(qry_str)

qry_str =  "select t.tran_secs, t.debit_amt "
qry_str += "from transactions as t, counterpartys as c "
qry_str += "where c.name = 'WAITROSE'"
qry_str += "and t.cpy_id = c.id "
qry_str += "order by 2"


qry_str  = "select tt.name, \n"
qry_str += "       t.debit_amt, \n"
qry_str += "       c.name \n"
qry_str += "from   transactions as t, \n"
qry_str += "       counterpartys as c, \n"
qry_str += "       transactiontypes as tt \n"
qry_str += "where  t.tran_secs > ( \n"
qry_str += "    select distinct secs \n"
qry_str += "    from   dateconversions \n"
qry_str += "    where  date = '18/07/2013') \n"
qry_str += "and    tran_secs < ( \n"
qry_str += "    select distinct secs \n"
qry_str += "    from   dateconversions \n"
qry_str += "    where  date = '23/07/2013') \n"
qry_str += "and    c.id = t.cpy_id \n"
qry_str += "and    tt.id = t.tt_id "
finance.run_qry(qry_str)

finance.close()
