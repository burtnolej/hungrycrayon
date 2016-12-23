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

#python ./ssviewer_rest.py --allow-unknown

class Test_Base():
    def setUp(self,dbname,port):
        self.dbname = dbname
        self.pid = os.getpid()
        self.url = URL + str(port) + "/"
        
    def _queryxml(self,buf,xpathstr,tag):
        tree_element = xmltree.fromstring(buf)
        xmlroot = ElementTree.ElementTree(tree_element) 
        return(xmlroot.findall(xpathstr))
    
    def _getelementstext(self,elements):
        return [element.find('value').text for element in elements]  
    
    
    def tearDown(self):
        shutil.copyfile(self.dbname+".backup",self.dbname)
        
class Test_View(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):
        
        self.expected_results = ['Humanities','Math','Humanities','??','Student News']
            
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                                   yaxis="dow",ztypes="subject",source_type="student",
                                   source_value="Clayton")    
            
        self.results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))

        
    def test_filter(self):

        self.expected_results = ['Math']
            
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                                   yaxis="dow",ztypes="subject",source_type="student",
                                   source_value="Clayton",cnstr_dow="MO")    

        self.results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        
    def test_update(self):

        self.expected_results = ['doodah']

        ssrest.restquery(self.url + "update/lesson",
                         subject="doodah",id="046CE5DA")    

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="MO")    
    
        self.results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))

    def test_multi(self):

        self.expected_results = ['doodah4']
                
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
    
        self.results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
                
    def assertListResult(self):
        if self.results == self.expected_results:
            print "PASSED"
        else:
            print "FAILED"
        
    def run(self,testname):
        self.setUp()
        getattr(self,testname)()
        self.assertListResult()
        self.tearDown()

if __name__ == "__main__":
        
    test = Test_View()
    test.run('test_')
    test.run('test_filter')
    test.run('test_update')
    test.run('test_multi')