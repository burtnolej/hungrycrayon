import sys
import os
from os import path as ospath
import shutil
from Tkinter import *
from ttk import *

import unittest
from database_util import Database
from database_table_util import tbl_rows_get
import ssviewer_rest
import ssviewer_rest_utils as ssrest

from misc_utils_process import process_kill, process_start, process_get_stdout

import pycurl
import cStringIO
import urllib

from time import sleep

import xml.etree.ElementTree as xmltree
from xml.etree import ElementTree

URL =  "http://0.0.0.0:"
APPROOT = os.environ['APPROOT']

class Test_Base(unittest.TestCase):
    def setUp(self,dbname,port):
        sleep(1)
        self.dbname = dbname
        self.pid = os.getpid()
        self.url = URL + str(port) + "/"
        
    def _queryxml(self,buf,xpathstr,tag):
        tree_element = xmltree.fromstring(buf)
        xmlroot = ElementTree.ElementTree(tree_element) 
        return(xmlroot.findall(xpathstr))
    
    def _getelementstext(self,elements):
        return [element.find('value').text for element in elements]        
        
class Test_View(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
        
        expected_results = ['Humanities','Math','Humanities','??','Student News']
            
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                               yaxis="dow",ztypes="subject",source_type="student",
                               source_value="Clayton")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)

    def test_filter(self):

        expected_results = ['Math']
            
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                               yaxis="dow",ztypes="subject",source_type="student",
                               source_value="Clayton",cnstr_dow="MO")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)

class Test_Update(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):

        expected_results = ['doodah']
                
        ssrest.restquery(self.url + "update/lesson",
                         subject="doodah",id="046CE5DA")    

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="MO")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
                
    def test_multi(self):

        expected_results = ['doodah4']
        
        ssrest.restquery(self.url + "update/lesson",
                         subject="doodah1",id="046CE5DA")
        ssrest.restquery(self.url + "update/lesson",
                         subject="doodah2",id="046CE5DA")
        ssrest.restquery(self.url + "update/lesson",
                         subject="doodah3",id="046CE5DA") 
        ssrest.restquery(self.url + "update/lesson",
                         subject="doodah4",id="046CE5DA") 

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="MO")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
                
    def tearDown(self):
        shutil.copyfile(self.dbname+".backup",self.dbname)

class Test_Add(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):

        expected_results =[[u'Clayton', u'??', u'Math', u'830-910', u'MO'], 
                           [u'Clayton', u'??', u'??', u'830-910', u'WE'], 
                           [u'Clayton', u'??', u'Student News', u'830-910', u'TH'], 
                           [u'Clayton', u'Amelia', u'Humanities', u'830-910', u'TU'], 
                           [u'Clayton', u'??', u'Humanities', u'830-910', u'FR'], 
                           [u'Clayton', u'Stan', u'Math', u'830-910', u'TU']]
                
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',adult='Stan',subject='Math',period='830-910',
                         recordtype='subject',dow='Tuesday')
        
        db = Database(self.dbname)
        
        with db:
            _,rows,_ = tbl_rows_get(db,'lesson',['student','teacher','subject','period','dow'])
       
        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        shutil.copyfile(self.dbname+".backup",self.dbname)
        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    ''' need to restart the rest service to run these tests again 
    killall python
    python ./ssviewer_rest.py --allow-unknown
    '''
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_View))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Update))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add))
    unittest.TextTestRunner(verbosity=2).run(suite) 