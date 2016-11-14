import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest
from ssloader import SSLoader
from ssviewer import WizardUI, dump2csv
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory
from xml_utils import grid2xml, xml2string
from misc_utils_process import process_kill, process_start, process_get_stdout


class Test_Viewer_Base(unittest.TestCase):
    
    def setUp(self,dbname,files=None):
        
        self.dbname = dbname
        
        if files <> None:
            create_test_db(self.dbname,files)
        self.database = Database(self.dbname)
        
        of = ObjFactory(True)
        self.app = WizardUI(self.dbname,of,self.dbname,maxentrycols=12,maxentryrows=20)
        
class Test_(Test_Viewer_Base):
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")

    def test_1row_1col_2subrow_1subcol(self):
    
        # dow=MO,period=830-910,student=Peter,ztype=adult
                            
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
            
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")
        
        xml = grid2xml(results,ids=True)
        
        phpexec = "/home/burtnolej/Development/pythonapps3/phpapps/apps/sswebviewer/xml2html.php"

        cmd = ['php',phpexec,xml2string(xml)]
        
        p = process_start(cmd)
        print process_get_stdout(p)
        
        #self.assertListEqual(results,expected_results)
        
    '''def test_Mo_830_910_Peter_adult_2attr(self):
                
        expected_results = [['', u'MO'], 
                            [u'830-910', [(dict(value='ELA',bgcolor='#ffcc99',fgcolor='black'),dict(value='Amelia',bgcolor='#006600',fgcolor='green'))]]]
                            
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="Peter",formatson=True)
        
        self.assertListEqual(results,expected_results)'''
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_))
    unittest.TextTestRunner(verbosity=2).run(suite) 