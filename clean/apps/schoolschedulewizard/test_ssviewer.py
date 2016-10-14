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

from shutil import copyfile
from os import remove, path
        
class Test_Nathaniel(unittest.TestCase):
    
    # uses a database loaded (via ssloader.run) from files prep4/5/6data.csv, staffdata.csv, academic.csv
    
    def setUp(self):
        self.databasename = "test_ssloader_all"
    
        of = ObjFactory(True)
        self.app = WizardUI(self.databasename,of,self.databasename,maxentrycols=12,maxentryrows=20)
        self.app.load(saveversion=1,student="Nathaniel")
        
          
    def test_(self):

        results = self.app.viewer(False,'student','Nathaniel',["subject","teacher"])
        
        expected_results = [["","MO","TU","TH","WE","FR"],                                                                                                                                                                                                                
                            ["830-910","ELA,Amelia","Math,Stan","Math,Stan","ELA,Amelia","Humanities,A"],                                                                                                                                                                                                     
                            ["910-950","Core,??","Work Period,Dylan","Core,??","Work Period,Moira","Music,??"],                                                                                                                                                                                               
                            ["950-1030","Work Period,Karolina","Activity Period,Aaron","Work Period,Issey","OT,??","STEM,??"],                                                                                                                                                                                
                            ["1030-1110","Activity Period,Dylan","Chess,Rahul","Chess,Rahul","Activity Period,Issey","Art,??"],                                                                                                                                                                               
                            ["1110-1210","Computer Time,??","Computer Time,??","Computer Time,??","Computer Time,??","Computer Time,??"],                                                                                                                                                                     
                            ["1210-100","Science,Paraic","History,Samantha","History,Samantha","Science,Paraic","??,??"],                                                                                                                                                                                         
                            ["100-140","Chess,Rahul","Work Period,Karolina","Work Period,Aaron","Chess,Rahul","??,??"],                                                                                                                                                                                            
                            ["140-220","Work Period,Johnny","Movement,??","Movement,??","Work Period,Issey","??,??"],                                                                                                                                                                                            
                            ["220-300","Speech,??","Student News,??","Student News,??","Counseling,Alexa","??,??"],                                                                                                                                                                                           
                            ["300-330","Computer Time,??","Computer Time,??","Computer Time,??","Computer Time,??","??,??"]]


        
        self.assertListEqual(expected_results,results)

    def tearDown(self):
        pass


class Test_Johnny(unittest.TestCase):
    
    # example of a multiple student in one session
    
    # uses a db copied from prod with all teachers, students in it
    
    def setUp(self):
        self.databasename = "test_ssloader_all"
    
        of = ObjFactory(True)
        self.app = WizardUI(self.databasename,of,self.databasename,maxentrycols=12,maxentryrows=20)
        self.app.load(saveversion=1,teacher="Johnny")
          
    def test_(self):

        results = self.app.viewer(False,'teacher','Johnny',["student"])
        
        expected_results = [['', u'MO', u'TU', u'TH', u'WE', u'FR'], 
                            [u'830-910', '??', u'Bruno,Orig,Oscar', u'Mackenzie', '??', '??'], 
                            [u'910-950', u'Clayton,Oscar,Stephen', u'Clayton', u'Asher,Shane', u'Lucy,Mackenzie,Nick', '??'],
                            [u'950-1030', u'Bruno', u'Jack,Peter', u'Luke,Simon B', u'Asher,Shane', '??'],
                            [u'1030-1110', u'Asher,Shane', u'Clayton,Stephen', u'Luke', '??', '??'],
                            [u'1110-1210', '??', '??', '??', '??', '??'],
                            [u'1210-100', u'Stephen', '??', '??', '??', '??'], 
                            [u'100-140', u'Oscar,Stephen', u'Liam,Oscar,Stephen', u'Asher,Shane', u'Nick,Shane', '??'], 
                            [u'140-220', u'Simon B', u'Clayton', u'Simon B', u'Shane', '??'],
                            [u'220-300', u'Bruno,Clayton,Orig,Peter', u'Bruno,Clayton,Jake,Orig', u'Luke,Simon B', u'Lucy', '??'],
                            [u'300-330', '??', '??', '??', '??', '??']]

        self.assertListEqual(expected_results,results)

    def tearDown(self):
        pass
    
    
class Test_Nathaniel_Conflict(unittest.TestCase):
    
    # uses a database loaded (via ssloader.run) from files prep4/5/6data.csv, staffdata.csv, academic.csv
    
    def setUp(self):
        self.databasename = "test_ssloader"
        
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.run(self.databasename, [('prep5data_test1period1Monday.csv',5,True),
                           ('prep5studentNathanielPeriod1.csv',-1,True)])  
    

        of = ObjFactory(True)
        self.app = WizardUI(self.databasename,of,self.databasename,maxentrycols=12,maxentryrows=20)
        self.app.load(saveversion=1,student="Nathaniel")

    def test_(self):    
        
        results = self.app.viewer(False,'student','Nathaniel',["subject","teacher"])

        print results
        
class Test_Get_Details(unittest.TestCase):
    
    # uses a database loaded (via ssloader.run) from files prep4/5/6data.csv, staffdata.csv, academic.csv
    
    def setUp(self):
        self.databasename = "test_ssloader"
        
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.run(self.databasename, [('prep5data_test1period1Monday.csv',5,True),
                           ('prep5studentNathanielPeriod1.csv',-1,True)])  
    

        of = ObjFactory(True)
        self.app = WizardUI(self.databasename,of,self.databasename,maxentrycols=12,maxentryrows=20)
        self.app.load(saveversion=1,student="Nathaniel")

    def test_(self):    
        
        self.app.viewer(True,'student','Nathaniel',["subject","teacher"])
        
        self.app.mainloop()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    # functional tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Get_Details))    
    
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Johnny))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


