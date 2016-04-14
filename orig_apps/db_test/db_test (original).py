

from sys import path,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView
from misc_util import Logger
from error_util import Notification
from stack_util import get_exception_info

class Football(Database):
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

#l = Logger("/private/tmp/log.txt")

football = Football("~/gadfly/scripts/","create")
gc = football.table(Grounds)
pc = football.table(Players)

gctr1 = [{'ground_name':'anfield','capacity':50000},
         {'ground_name':'walkers stadium','capacity':30000}]

pctr1 = [{'last_name':'bale','goals':0,'debut':'1/10/13'},
         {'last_name':'messi','goals':1500,'debut':'1/12/13'},
         {'last_name':'lopez','goals':60,'debut':'2/10/13'}]


gc.add_list(gctr1)
pc.add_list(pctr1)
football.init_objects_in_db()

football.commit_to_gf()

football.run_qry("select * from Players")
football.run_qry("select * from Grounds")
football.run_qry("select * from __datadefs__")

football.close()
del gc,pc
#del l
