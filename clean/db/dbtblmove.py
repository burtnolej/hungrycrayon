
import sys
from os import remove

from database_util import Database, tbl_exists
from database_table_util import tbl_move

if len(sys.argv) <> 4:
    print "usage: dbtblmove.py dbsource dbtarget tblname"
    print
    print "e.g. python ./dbtblmove.py fucia.sqlite quad.sqlite formats"
    exit()
    
argvnames = ['dbsource','dbtarget','tblname']
args = dict(zip(argvnames,sys.argv[1:]))

dbtarget = Database(args['dbtarget'])

with dbtarget:
    if tbl_exists(dbtarget,args['tblname']) == True:
        print "table ",args['tblname']," already exists in db ",args['dbtarget']
        exit()

tbl_move(Database(args['dbsource']),
         Database(args['dbtarget']),
         args['tblname'])

with dbtarget:
    if tbl_exists(dbtarget,args['tblname']) == True:
        print "table ",args['tblname']," moved to db ",args['dbtarget']
        
