import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest

from sswizard import schoolschedgeneric, WizardUI
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory

from shutil import copyfile
from os import remove, path

class Test_Base(unittest.TestCase):
    def setUp(self,dbname,refdbname):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = dbname
        self.dbfilename = path.join(dbpath,self.dbname)
        self.database = Database(self.dbfilename)
        self.of = ObjFactory(True)
        self.ui = WizardUI(self.dbname, self.of,refdbname)       
        self.ui.dbname_entry_sv.set(dbname)
        
        parent_name = self.ui.entrygrid.widgets[0][0].winfo_parent()
        self.parent_widget = self.ui.entrygrid.widgets[0][0]._nametowidget(parent_name)
        self.parent_widget.update()

    def tearDown(self):
        self.ui.destroy()
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        
class Test_Input_New_Save_Persist(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'tmp','test_quadref')
    
        self.ui.dbname_entry_sv.set(self.dbname)
    
        self.ui.entrygrid.widgets[1][0].sv.set('Nathaniel')
        self.ui.entrygrid.widgets[0][1].sv.set('830-910')
        self.ui.entrygrid.widgets[1][1].sv.set('AMEL.AC.ELA.MO')
    
        self.ui.save(1)
        self.ui.persist()
          
    def test_dbwrite(self):
        
        expected_result = [['830-910', u'Nathaniel','AMEL.AC.ELA.MO', u'MO', '1']]
        
        cols = ['period','student','session','dow','saveversion']

        with self.database:
            colndefn,rows,exec_str = tbl_rows_get(self.database,'lesson',cols,
                                                  [['saveversion',"=",'1']])
        
        self.assertListEqual(expected_result,rows)

    def tearDown(self):
        self.ui.destroy()
        os.remove(self.dbname+".sqlite")

      
                
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load))    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


