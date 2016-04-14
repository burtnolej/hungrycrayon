#!/usr/bin/python

from sys import path,argv,exit
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Logger
from test_util import UnitTest, DBTestFailed
#from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView
from db_util import *
from error_util import Notification
from stack_util import get_exception_info
from functools import wraps
    
def _test_dec(perm,test_exp_res,exc=None,**kwargs):
    '''
    perm : string create|use
    test_exp_res : expected records to find in db
    exc : expected exception - optional (for -ve testing)
    dbcls : used to specify an in existing gf instance to use
    ''' 
    def actual_dec(func):
        @wraps(func)
        #def wrapper(*args, **kwargs):
        def wrapper():
            test_name = func.__name__[6:]
            try:
                if kwargs.has_key('dbcls'):
                    db = kwargs['dbcls'](GFDIR,perm)
                else:
                    db = Test(GFDIR,perm)

                ut = UnitTest.db_test(db,test_name)
                func(db)
                #db.pprint()
                db.init_objects_in_db()
                db.commit_to_gf()
                ut.check_dbresults(test_exp_res)
                # if code gets here then pass/+ve
                return("PASSED:TESTCASE " + ut.name)
            except exc: # test for expected exception pass/-ve
                return("PASSED:TESTCASE " + ut.name)
            except DBTestFailed,e: # failure
                return("FAILED:TESTCASE " + str(ut.name) + str(e))
            finally:
                db.close()
        return wrapper
    return actual_dec

class Football(Database):
    pass

class Test(Database):
    pass

class Test_gp1(Database):
    pass

class Grounds(DatabaseTable):
    def __init__(self,*args,**kwargs):
        super(Grounds,self).__init__(*args,**kwargs)
        self._PKEY = "ground_name"

    def ground(self,**kwargs):
        g = Ground(**kwargs)
        self[kwargs.__getitem__('ground_name')] = g

class Ground(DatabaseRecord):
    pass

class Player(DatabaseRecord):
    pass

class Players(DatabaseTable):
    def __init__(self,*args,**kwargs):
        super(Players,self).__init__(*args,**kwargs)
        self._PKEY = "last_name"

    def player(self,**kwargs):
        p = Player(**kwargs)
        self[kwargs.__getitem__('last_name')] = p

gctr1 = {'table':'grounds',
         'records':[{'ground_name':'anfield',
                    'capacity':50000}],
         'pk':'ground_name'}
pctr1 = {'table':'players',
         'records':[{'last_name':'bale',
                    'goals':0,
                    'debut':'1/10/13'}],
         'pk':'last_name'}
gctr2 = {'table':'grounds',
         'records':[{'ground_name':'stamford bridge',
                    'capacity':55000}],
        'pk':'ground_name'}
pctr2 = {'table':'players',
         'records':[{'last_name':'rooney',
                    'goals':200,
                    'debut':'3/10/00'}],
         'pk':'last_name'}
gctr3 = {'table':'grounds',
         'records':[{'ground_name':'stamford bridge',
                     'capacity':15000}],
        'pk':'ground_name'}
pctr3 = {'table':'players',
         'records':[{'last_name':'rooney',
                    'goals':300,
                    'debut':'3/10/99'}],
        'pk':'last_name'}
pctr4 = {'table':'players',
         'records':[{'last_name':'rooney',
                    'goals':300,
                    'debut':'3/10/00'}],
        'pk':'last_name'}

pctr5 = {'table':'players',
        'pk':'last_name'}

GFDIR = "~/Downloads/gadflyZip/gadfly/scripts/"


#@_test_dec('create',[gctr1,pctr1])
@_test_dec('create',[gctr2,pctr2],dbcls=Test_gp1)
def _test_create_pos(db):
    '''
    test case : create db and tables, test for +ve result
    '''
    gc = db.table(Grounds)
    pc = db.table(Players)
    gc.add_list(gctr2['records'])
    pc.add_list(pctr2['records'])

@_test_dec('create',[gctr2,pctr2],exc=DBTestFailed)
def _test_create_neg(db):
    gc = db.table(Grounds)
    pc = db.table(Players)
    gc.add_list(gctr1['records'])
    pc.add_list(pctr1['records'])

@_test_dec('create',[],exc=DBErrorZeroDataRecords)
def _test_create_no_data(db):
    gc = db.table(Grounds)
    pc = db.table(Players)

@_test_dec('create',[gctr1,pctr1])
def _test_create_insert(db):
    gc = db.table(Grounds)
    pc = db.table(Players)
    gc.add_list(gctr1['records'])
    pc.add_list(pctr1['records'])
    #football.init_objects_in_db()
    gc.add_list(gctr2['records'])
    pc.add_list(pctr2['records'])

@_test_dec('use',[gctr3,pctr3],dbcls=Test_gp1)
def _test_use_update_multi_ins(db):
    gc = db.table(Grounds)
    pc = db.table(Players)
    gc.pprint()
    gc.add_list(gctr3['records'])
    pc.add_list(pctr3['records'])


test_schedule = ['create_pos',
                 'create_neg',
                 'create_no_data',
                 #'create_insert',
                 'use_update_multi_ins',
                 ]

if len(argv) == 1:
    print "defined testcases are :"
    for test in test_schedule:
        #print locals()["_test_" + test]()
        print locals()["_test_" + test].__name__
else:
    if argv[1] == 'sched':
        for test in test_schedule:
            print locals()["_test_" + test]()
    elif argv[1] == 'all':
        for test in locals().iteritems():
            if str(test).startswith("_test_"):
                print locals()["_test_" + test]()
    elif locals()["_test_" + argv[1]]:
        print locals()["_test_" + argv[1]]()
    else:
        print "do not recognise test case ",argv[1]

exit()

## TEST CASE ########################################
try:
    football = Football(GFDIR,'create')
    gc = football.table(Grounds)
    pc = football.table(Players)
    gc.add_list(gctr2['records'])
    pc.add_list(pctr2['records'])
    football.init_objects_in_db()
    football.commit()
except:
    raise
finally:
    football.close()
    del football

try:
    football = Football(GFDIR,'use')            
    ut = UnitTest.db_test(football,'use, update multiple fields by inserting new')
    gc = football.table(Grounds)
    pc = football.table(Players)
    football.init_objects_in_db()
    gc.add_list(gctr3['records'])
    pc.add_list(pctr3['records'])
    football.commit()
    ut.check_dbresults([pctr3,gctr3])
    print "PASSED:TESTCASE",ut.name
except DBTestFailed,e: # functional test failed 
    print "FAILED:TESTCASE",ut.name,e
except: # unknown error caused failed
    e = get_exception_info()
    Notification.enrich(e['value'])
    print "FAILED:TESTCASE",ut.name,"unknown"
finally:
    football.close()
    del football

## TEST CASE ########################################
pctr2 = {'table':'players',
         'records':[{'last_name':'rooney',
                    'goals':200,
                    'debut':'3/10/00'}],
         'pk':'last_name'}    
try:
    football = Football(GFDIR,'create')
    pc = football.table(Players)
    pc.add_list(pctr2['records'])
    football.init_objects_in_db()
    football.commit()
except:
    raise
finally:
    football.close()
    del football

try:
    football = Football(GFDIR,'use') #loading then updating
    ut = UnitTest.db_test(football,'use, update multiple fields by updating record')
    pc = football.table(Players)
    football.init_objects_in_db()
    pc.update_rec('rooney','goals',300)
    football.commit()
    ut.check_dbresults([pctr4])
    print "PASSED:TESTCASE",ut.name
except DBTestFailed,e: # functional test failed
    print "FAILED:TESTCASE",ut.name,e
except: # unknown error caused failed
    e = get_exception_info()
    Notification.enrich(e['value'])
    print "FAILED:TESTCASE",ut.name,"unknown"
finally:
    football.close()
    del football

## TEST CASE ########################################
pctr2 = {'table':'players',
         'records':[{'last_name':'rooney',
                    'goals':200,
                    'debut':'3/10/00'}],
         'pk':'last_name'}    
try:
    football = Football(GFDIR,'create')
    pc = football.table(Players)
    pc.add_list(pctr2['records'])
    football.init_objects_in_db()
    football.commit()
except:
    raise
finally:
    football.close()
    del football

try:
    football = Football(GFDIR,'use') #loading then updating
    ut = UnitTest.db_test(football,'use, delete record')
    pc = football.table(Players)
    football.init_objects_in_db()
    pc.delete_rec('rooney')
    football.commit()
    ut.check_dbresults([pctr5])
    print "PASSED:TESTCASE",ut.name
except DBTestFailed,e: # functional test failed 
    print "FAILED:TESTCASE",ut.name,e
except: # unknown error caused failed
    e = get_exception_info()
    Notification.enrich(e['value'])
    print "FAILED:TESTCASE",ut.name,"unknown"
finally:
    Notification.print_summary()
    football.close()
    del football

#qry_str =  "select * \n"
#qry_str += "from   players"
#football.run_qry(qry_str)
#football.execute(qry_str)
#for res in football.fetchall():
#    print res

#print football.description()

#for res in football.fetchall_like('last_name','^b.*'):
#    print res

#pc.pprint()
#gc.pprint()

del l

