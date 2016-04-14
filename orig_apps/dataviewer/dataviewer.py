#!/usr/bin/python

from sys import path,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Singleton, get_time_hms, in_method_log, Logger, file2list
from ui_util import ListBox,EntryBox,TextBox,WindowManager,DocBox,Window,DebugBox
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView
from error_util import Notification
from stack_util import get_exception_info
import thread_util 
import curses
import time

class Finance(Database):
    pass

def main(screen):
    try:    
        screen.keypad(1)
        curses.mousemask(1)
        curses.nonl()

        l = file2list("doc.txt")

        finance = Finance("~/Downloads/gadflyZip/gadfly/scripts/",'use')
    
        cn = finance.view(CounterpartyNames)
        tv = finance.view(TransactionView)
        #nt = finance.table(NoteTable)
    
        finance.loadviews()

        wm = WindowManager()
        lb = CounterpartyNamesLB.dbitems(wm,"lb1",20,30,5,10,cn)
        lb.daemon = True
        lb.start()
        lb.parent = None
        lb.name = "lb1"
    
        lb2 = TransactionViewLB.dbitems(wm,"lb2",20,30,5,40,tv)
        lb2.daemon = True
        lb2.start()
        lb2.parent = "lb1"
        lb2.name = "lb2"
    
        eb = CounterpartyNamesFilterEB(wm,"eb1",3,30,27,10)
        eb.daemon = True
        eb.start()
        eb.parent = "lb1"
        eb.name = "eb1"

        #db = DebugBox(wm,"db",10,50,26,5,True)
        #db.daemon = True
        #db.start()
        #db.name = "db"

        db1 = MyDocsDB.listitems(wm,"db1",1,60,32,10,l)
        db1.daemon = True
        db1.start()
        db1.parent = "db1"
        db1.name = "db1"

        wm.mainloop()
    except KeyboardInterrupt:
        print "Got KeyboardInterrupt exception. Exiting..."
        exit()
    except AssertionError:
        e = get_exception_info()
        Notification.enrich(e['value'])
        exit()
    except:
        e = get_exception_info()
        
        Notification.enrich(e['value'])
        exit()
    finally:
        Notification.print_summary()

class MyDocsDB(DocBox):
    #def context_event_handler(self,event):
    #    pass
    
    def run(self):
        while 1:
            time.sleep(0.1)
    
class CounterpartyNamesLB(ListBox):
    def context_event_handler(self,event):
        if event in [curses.KEY_DOWN,curses.KEY_UP]:
            (text,_,_) = tuple(self._items_sel())
            qm = thread_util.QueueMessage("lb2",sender=self.name,payload=text)
            qm.pprint("put",self.name)
            with thread_util.threadLock:
                thread_util.MyThread.myQueue.put(qm)
        return False

    def run(self):
        while 1:
            thread_util.MyThread.check_q(self.name,self._filter_dbitems)            
            time.sleep(0.1)

class TransactionViewLB(ListBox):
    def run(self):
        while 1:
            thread_util.MyThread.check_q(self.name,self._reload_dbitems)            
            time.sleep(0.1)

class CounterpartyNamesFilterEB(EntryBox):
    def context_event_handler(self,event):
        print event
        if event == 10:
            qm = thread_util.QueueMessage("lb1",sender=self.name,payload=self._current_str)
            qm.pprint("put",self.name)
            with thread_util.threadLock:
                thread_util.MyThread.myQueue.put(qm)
        return False

class CounterpartyNames(DatabaseView):
    def init_load(self,arg=None,re=None):
        init_load_qry  = "select name "
        init_load_qry += "from   counterpartys "
        init_load_qry += "order by name"
        self.__load(init_load_qry,re)
        
    def __load(self,qry,re=None):
        self.db.execute(qry)
        for col1 in self.db.fetchall():
            #window constructor needs a rec field called display_text
            self.add(cpy_name = str(col1),display_text=str(col1))

    def add(self,**kwargs):
        dr = DatabaseRecord(**kwargs)
        self[dr.cpy_name] = dr
        
class TransactionView(DatabaseView):
    def init_load(self,arg=None,re=None):
        init_load_qry  = "select tran_date,debit_amt,c.name "
        init_load_qry += "from   transactions, "
        init_load_qry += "       counterpartys as c "
        init_load_qry += "where  c.id = cpy_id "
        if arg:
            init_load_qry += "and    c.name = '" + arg + "'"
        
        self.__load(init_load_qry,re)
        
    def __load(self,qry,re=None):
        print qry
        self.db.execute(qry)
        self.clear()
        for col1,col2,col3 in self.db.fetchall():
            self.add(tran_date = str(col1),
                     debit_amt = str(col2),
                     c_name = str(col3),
                     display_text=str(str(col1) + " " + str(col2)))
        
    def add(self,**kwargs):
        dr = DatabaseRecord(**kwargs)
        self[dr._id] = dr

logger = Logger("/tmp/log.txt")
curses.wrapper(main)
logger.__del__()
