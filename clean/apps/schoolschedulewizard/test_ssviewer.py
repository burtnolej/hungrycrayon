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

def create_test_db(dbname,files):
    #filename,prep):
    #database = Database(dbname)
    #files = [(filename,prep,True)]
    ssloader = SSLoader(dbname)
    ssloader.run(dbname,files)
    
class Test_Viewer_Base(unittest.TestCase):
    
    def setUp(self,dbname,files=None):
        
        self.dbname = dbname
        
        if files <> None:
            create_test_db(self.dbname,files)
        self.database = Database(self.dbname)
        
        of = ObjFactory(True)
        self.app = WizardUI(self.dbname,of,self.dbname,maxentrycols=12,maxentryrows=20)
    
'''
if the tests fail and in the logs in says cannot find table "recordtype", this is because
some of the test databasese still use lesson_type (static table manually created)
the quad.sqlite in ../schoolscheduler will have a table called recordtype so 
cp ../schoolscheduler/quad.sqlite test_ssloader.sqlite and then un comment the line
with a files argument and then just uncomment the test_ function to regenerate the correct
test data

also the tests may expect the old periods, so 1210-100,100-140,140-220,220-300,300-330

same goes for Test_Viewer_Conflicts_master_record;  same instruxx as above
'''

class Test_Viewer_X_Period_Y_DOW(Test_Viewer_Base):
    
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssloader",[("prep5student.csv",5,True)])
        Test_Viewer_Base.setUp(self,"test_ssloader")
    
    '''def test_(self):
        pass'''
    
    def test_Mo_830_910_Peter_adult_subject(self):
        
        expected_results = [['', u'MO'], [u'830-910', [(u'Amelia', u'ELA')]]]
        
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['adult','subject'],source_type="student",source_value="Peter")
    
        self.assertListEqual(results,expected_results)
        
    
    def test_Mo_Peter_adult_subject(self):
        
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
        
        expected_results = [['', u'MO'],[u'1030-1110',[(u'Jake', u'Aaron'), (u'Peter', u'Issey'), (u'Orig', u'??'), (u'Bruno', u'Dylan'), (u'Oscar', u'Paraic'), (u'Clayton', u'Dylan'), (u'Jack', u'Paraic'), (u'Nathaniel', u'Amelia'), (u'Stephen', u'??')]]]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['student','adult'],source_type="student",source_value="")
        
        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_count_groupby(self):
        
        expected_results = [['', u'MO'], [u'1030-1110', [8]]]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['*'],source_type="student",source_value="")

        self.assertListEqual(results,expected_results)

        
class Test_Viewer_X_Period_Y_Adult(Test_Viewer_Base):
    
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssloader","prep5student.csv",5,True)
        Test_Viewer_Base.setUp(self,"test_ssloader")

    def test_Karolina_Peter_adult_subject(self):
        
        expected_results = [['', u'Karolina'], [u'140-220', [(u'Peter', u'Counseling')]]]
        
        self.app.load(saveversion=1,student="Peter",teacher="Karolina")

        results = self.app.viewer(ui=False,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult")
        
        self.assertListEqual(results,expected_results)
        
    def test_830_910_Peter_adult_subject(self):
        
        expected_results = [['', u'??', u'Karolina', u'Paraic', u'Issey', u'[Paraic,Rahul]', u'Amelia'], 
                            [u'830-910', [], [], [], [], [], [(u'Peter', u'ELA')]], 
                            [u'910-950', [(u'Peter', u'Core')], [], [], [], [], []], 
                            [u'950-1030', [], [], [(u'Peter', u'Science')], [], [], []], 
                            [u'1030-1110', [], [], [], [(u'Peter', u'History')], [], []], 
                            [u'1110-1210', [(u'Peter', u'Computer Time')], [], [], [], [], []], 
                            [u'1210-100', [], [], [], [], [(u'Peter', u'??')], []], 
                            [u'100-140', [], [], [], [], [], [(u'Peter', u'ELA')]], 
                            [u'140-220', [], [(u'Peter', u'Counseling')], [], [], [], []], 
                            [u'220-300', [(u'Peter', u'Movement')], [], [], [], [], []], 
                            [u'300-330', [(u'Peter', u'Computer Time')], [], [], [], [], []]]

        self.app.load(saveversion=1,student="Peter",dow="MO")

        results = self.app.viewer(ui=False,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult")

        self.assertListEqual(results,expected_results)
        
class Test_Viewer_Conflicts_master_record(Test_Viewer_Base):
    
    def setUp(self):

        files = [("prep5studentPeterPeriod1.csv",5,True),("prep56new_Amelia_1period.csv",-1,True)]
        
        #Test_Viewer_Base.setUp(self,"test_ssloader_conflicts",files)
        Test_Viewer_Base.setUp(self,"test_ssloader_conflicts")

    def test_(self):
        
        self.app.load(saveversion=1,student="Peter")

        expected_results = [['', u'MO', u'TU', u'FR', u'WE', u'TH'], 
                            [u'830-910', [(u'MO', u'Math', u'subject')], [(u'TU', u'[Activity Period,ELA]', u'[subject,wp]')], 
                             [(u'FR', u'Humanities', u'subject')], [(u'WE', u'Math', u'subject')], [(u'TH', u'Student News', u'subject')]]]
        
        results = self.app.viewer(ui=False,ztypes=['dow','subject','recordtype'],source_type="student",source_value="Peter")

        self.assertListEqual(results,expected_results)
        
class Test_Viewer_Conflicts(Test_Viewer_Base):
    
    def setUp(self):

        files = [("prep5studentPeterPeriod1.csv",5,True,"5s"),("prep56new_Amelia_1period.csv",-1,True,"56n")]
        
        Test_Viewer_Base.setUp(self,"test_ssloader_conflicts",files)

    def test_(self):
        
        self.app.load(saveversion=1,student="Peter",source="56n,5s")

        expected_results = [['', u'FR', u'MO', u'TU', u'WE', u'TH'], 
                            [u'830-910', [(u'Humanities',)], [(u'Math',)], [(u'Activity Period',), (u'ELA',)], 
                             [(u'Math',)], [(u'Student News',)]]]

        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="Peter")
        self.assertListEqual(results,expected_results)
        
class Test_Viewer_UI(Test_Viewer_Base):
    
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssloader",[("prep5student.csv",5,True)])
        Test_Viewer_Base.setUp(self,"test_ssloader")
        
    def test_Mo_830_910_Peter_adult_subject(self):
        
        expected_results = [['', u'MO'], [u'830-910', u'(Amelia,ELA)']]
        
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        self.app.viewer(ui=True,ztypes=['adult','subject'],source_type="student",source_value="Peter")

        results = self.app._dumpviewergrid()
        
        self.assertListEqual(results,expected_results)
            
    def test_Peter_student_subject(self):
        
        expected_results = [['', u'??', u'Karolina', u'Paraic', u'Issey', u'[Paraic,Rahul]', u'Amelia'], 
                            [u'830-910', '', '', '', '', '', u'(Peter,ELA)'], 
                            [u'910-950', u'(Peter,Core)', '', '', '', '', ''], 
                            [u'950-1030', '', '', u'(Peter,Science)', '', '', ''], 
                            [u'1030-1110', '', '', '', u'(Peter,History)', '', ''], 
                            [u'1110-1210', u'(Peter,Computer Time)', '', '', '', '', ''], 
                            [u'1210-100', '', '', '', '', u'(Peter,??)', ''], 
                            [u'100-140', '', '', '', '', '', u'(Peter,ELA)'], 
                            [u'140-220', '', u'(Peter,Counseling)', '', '', '', ''], 
                            [u'220-300', u'(Peter,Movement)', '', '', '', '', ''], 
                            [u'300-330', u'(Peter,Computer Time)', '', '', '', '', '']]

        self.app.load(saveversion=1,student="Peter",dow="MO")

        self.app.viewer(ui=True,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult")

        results = self.app._dumpviewergrid()

        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_count_groupby(self):
        
        expected_results = [['', u'MO'], [u'1030-1110', '8']]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        self.app.viewer(ui=True,ztypes=['*'],source_type="student",source_value="")

        results = self.app._dumpviewergrid()

        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_groupby(self):
        
        expected_results = [['', u'MO'], [u'1030-1110', u'(ELA,Aaron)(History,Issey)(Core,??)(Game Period,Dylan)(Science,Paraic)(Game Period,Dylan)(Science,Paraic)(ELA,Amelia)(Core,??)']]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        self.app.viewer(ui=True,ztypes=['subject','adult'],source_type="student",source_value="")

        results = self.app._dumpviewergrid()
        
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        self.app.destroy()
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_DOW))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_Adult))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Conflicts_master_record))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Conflicts))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_UI))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


