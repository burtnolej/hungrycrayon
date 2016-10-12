import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest

from ssviewer import WizardUI
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory

from shutil import copyfile
from os import remove, path
        
class Test_Nathaniel(unittest.TestCase):
    
    # uses a database loaded (via ssloader.run) from files prep4/5/6data.csv, staffdata.csv, academic.csv
    
    def setUp(self):
        self.databasename = "test_ssloader"
    
        of = ObjFactory(True)
        self.app = WizardUI(self.databasename,of,self.databasename,maxentrycols=12,maxentryrows=20)
        self.app.load(saveversion=1,student="Nathaniel")
        
          
    def test_(self):

        results = self.app.viewer(False)
        
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

      
                
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    # functional tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Nathaniel))    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


