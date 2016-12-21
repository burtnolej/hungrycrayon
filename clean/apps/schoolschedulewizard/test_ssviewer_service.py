import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest
from database_util import Database
from database_table_util import tbl_rows_get

from misc_utils_process import process_kill, process_start, process_get_stdout

import pycurl

#curl --get -d "ztypes=subject;xaxis=period;yaxis=dow" http://0.0.0.0:8080/student/Nathaniel

#curl --get http://0.0.0.0:8080/command/stop

class Test_Service_Base(unittest.TestCase):
    
    def setUp(self,dbname,files=None):
        
        APPROOT = os.environ['APPROOT']
        DBPATH = os.path.join(APPROOT,"clean","apps","schoolschedulewizard")
        os.environ['DBPATH'] = DBPATH
        
        APP = os.path.join(os.environ['DBPATH'],"ssviewer_rest.py")
        
        os.environ['DBNAME'] = dbname
        
        DB = os.path.join(DBPATH,dbname)
        
        cmd = [APP,DB]

        
        
class Test_(Test_Service_Base):
    
    def setUp(self):
        Test_Service_Base.setUp(self,"test_ssviewer_service")

    def test_(self):
        
        #getfields = []
        c = pycurl.Curl()
        c.setopt(c.URL, "http://0.0.0.0:8080/command/stop")
        c.setopt(c.VERBOSE,True)
        #c.setopt(c.HTTPHEADER,[header])
        #c.GETFIELDS,getfields)

        c.setopt(c.WRITEDATA, buffer)       
        c.perform()
        c.close()     
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_))
    unittest.TextTestRunner(verbosity=2).run(suite) 