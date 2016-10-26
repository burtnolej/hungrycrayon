import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest
from ssloader import SSLoader
from ssviewer import WizardUI
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory

def create_test_db(dbname,filename,prep):
    database = Database(dbname)
    files = [(filename,prep,True)]
    ssloader = SSLoader(dbname)
    ssloader.run(dbname,files)
    
class Test_Viewer_Base(unittest.TestCase):
    
    def setUp(self,dbname,filename=None,prep=None,createdb=False):
        
        self.dbname = dbname
        
        if createdb == True:
            create_test_db(self.dbname,filename)
        self.database = Database(self.dbname)
        
        of = ObjFactory(True)
        self.app = WizardUI(self.dbname,of,self.dbname,maxentrycols=12,maxentryrows=20)
        
class Test_Viewer_X_Period_Y_DOW(Test_Viewer_Base):
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"test_ssloader","prep5student",5)
        
    def test_(self):
        pass
    
    def test_Mo_830_910_Peter_adult_subject(self):
        
        expected_results = [['', u'MO'], [u'830-910', [(u'Amelia', u'ELA')]]]
        
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['adult','subject'],source_type="student",source_value="Peter")
    
        print results
        #self.assertListEqual(results,expected_results)
        
    '''def test_Mo_Peter_adult_subject(self):
        
        expected_results = [['', u'MO'], [u'830-910', [(u'Amelia', u'ELA')]], [u'910-950', [(u'??', u'Core')]],
                            [u'950-1030', [(u'Paraic', u'Science')]],[u'1030-1110', [(u'Issey', u'History')]], 
                            [u'1110-1210', [(u'??', u'Computer Time')]], [u'1210-100', [(u'[Paraic,Rahul]', u'??')]], 
                            [u'100-140', [(u'Amelia', u'ELA')]], [u'140-220', [(u'Karolina', u'Counseling')]], 
                            [u'220-300', [(u'??', u'Movement')]], [u'300-330', [(u'??', u'Computer Time')]]]

        self.app.load(saveversion=1,student="Peter",dow="MO")

        results = self.app.viewer(ui=False,ztypes=['adult','subject'],source_type="student",source_value="Peter")
        
        self.assertListEqual(results,expected_results)
    
    def test_Mo_830_910_Peter_adult_recordtype(self):
        
        expected_results = [['', u'MO'], [u'1030-1110', [(u'Issey', u'wp')]]]
        
        self.app.load(saveversion=1,student="Peter",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['adult','recordtype'],source_type="student",source_value="Peter")

        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_adult_subject(self):
        
        expected_results = [['', u'MO'], [u'1030-1110', [(u'Jake', u'Aaron'), (u'Peter', u'Issey'), (u'Orig', u'??'), (u'Bruno', u'Dylan'), (u'Oscar', u'Paraic'), 
                                                         (u'Clayton', u'Dylan'), (u'Jack', u'Paraic'), (u'Nathaniel', u'Amelia'), (u'Stephen', u'??')]]]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['student','adult'],source_type="student",source_value="")
        
        self.assertListEqual(results,expected_results)'''
        
class Test_Viewer_X_Period_Y_Adult(Test_Viewer_Base):
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"test_ssloader")
        
    def test_Karolina_Peter_adult_subject(self):
        
        expected_results = [['', u'Karolina'], [u'140-220', [(u'Peter', u'Counseling')]]]
        
        self.app.load(saveversion=1,student="Peter",teacher="Karolina")

        results = self.app.viewer(ui=False,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult")

        self.assertListEqual(results,expected_results)
        
    def test_830_910_Peter_adult_subject(self):
        
        expected_results = [['', u'??', u'Karolina', u'Paraic', u'Issey', u'[Paraic,Rahul]', u'Amelia'], 
                            [u'910-950', [(u'Peter', u'Core')]], 
                            [u'1110-1210', [(u'Peter', u'Computer Time')]], 
                            [u'220-300', [(u'Peter', u'Movement')]], 
                            [u'300-330', [(u'Peter', u'Computer Time')]], 
                            [u'140-220', [(u'Peter', u'Counseling')]], 
                            [u'950-1030', [(u'Peter', u'Science')]], 
                            [u'1030-1110', [(u'Peter', u'History')]], 
                            [u'1210-100', [(u'Peter', u'??')]], 
                            [u'830-910', [(u'Peter', u'ELA')]], 
                            [u'100-140', [(u'Peter', u'ELA')]]]

        
        self.app.load(saveversion=1,student="Peter",dow="MO")

        results = self.app.viewer(ui=False,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult")

        print results
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_DOW))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_Adult))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


