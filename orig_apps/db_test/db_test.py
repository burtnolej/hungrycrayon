from sys import path,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView
from misc_util import Logger
from error_util import Notification
from stack_util import get_exception_info

class Football(Database):
    pass

class MyClass3(object):
    pass

class Grounds(DatabaseTable):
    def __init__(self,*args,**kwargs):
        super(Grounds,self).__init__(*args,**kwargs)
        self._set_pk("ground_name")

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
        self._set_pk("last_name")

    def player(self,**kwargs):
        p = Player(**kwargs)
        self[kwargs.__getitem__('last_name')] = p

def create_db(db,_grounds,_players):
    grounds = db.table(Grounds)
    players = db.table(Players)
    grounds.add_list(_grounds)
    players.add_list(_players)
    db.init_objects_in_db()

def update_db(db):
    grounds = db.table(Grounds)
    players = db.table(Players)
    db.init_objects_in_db()
    players.update_rec('messi','goals',666)

l = Logger('/tmp/log.txt')

football = Football("~/gadfly/scripts/","auto")
football.execute("select * from PLayers")
print football.fetchall_num_rows()
exit()

g = [{'ground_name':'anfield','capacity':50000},
    {'ground_name':'walkers stadium','capacity':30000}]

p = [{'last_name':'bale','goals':0,'debut':'1/10/13'},
    {'last_name':'messi','goals':1500,'debut':'1/12/13'},
    {'last_name':'lopez','goals':60,'debut':'2/10/13'}]

if football._type == 'create':
    create_db(football,g,p)
elif football._type == 'use':
    update_db(football)

football.commit_to_gf()



#football.run_qry("select * from Grounds")
#football.run_qry("select * from __datadefs__")

football.close()

football.logmeta.pprint(l.stk_log_handle)
