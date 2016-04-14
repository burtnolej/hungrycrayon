
from gadfly import gadfly
import os, shutil

connect = gadfly()
if os.path.exists('_finances'):
    shutil.rmtree('_finances')
os.makedirs('_finances')

'''
tran
  tran_date    datetime
  tran_type_id integer
  cparty_id    integer
  ccy_id       integer

tran_type
  id           integer
  name         varchar
  desc         varchar
  
cparty
  id           integer
  name         varchar
  type         varchar

ccy
  id           integer
  name         integer
'''

type = {'POS - ':'POS',
        'DIRECT DEBIT - ':'DD',
        'CHAPS PAYMENT (ONLINE) ':'CHAPS',
        'STANDING ORDER TO ':'SO',
        'BACS PAYMENT FROM ':'BACS'}


connect.startup("finances","_finances")
curs = connect.cursor()
curs.execute('create table transactions (tran_date datetime, tran_type = varchar, counterparty)')
