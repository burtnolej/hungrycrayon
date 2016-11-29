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
import sswizard_utils
import ssviewer_utils

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
        
        #self.app.mainloop()
        
        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_count_groupby(self):
        
        expected_results = [['', u'MO'], [u'1030-1110', [8]]]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['*'],source_type="student",source_value="")

        self.assertListEqual(results,expected_results)
        
        
    def test_Mo_830_910_adult_subject_no_unknowns(self):
        
        expected_results = [['', u'MO'],[u'1030-1110',[(u'Jake', u'Aaron'), (u'Peter', u'Issey'), (u'Bruno', u'Dylan'), (u'Oscar', u'Paraic'), (u'Clayton', u'Dylan'), (u'Jack', u'Paraic'), (u'Nathaniel', u'Amelia')]]]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110",unknown='N')

        results = self.app.viewer(ui=False,ztypes=['student','adult'],source_type="student",source_value="")
        
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
        
        #Test_Viewer_Base.setUp(self,"test_ssloader_conflicts",files)
        Test_Viewer_Base.setUp(self,"test_ssloader_conflicts")

    '''def test_(self):
        
        self.app.load(saveversion=1,student="Peter",source="56n,5s")

        expected_results = [['', u'FR', u'MO', u'TU', u'WE', u'TH'], 
                            [u'830-910', [(u'Humanities',)], [(u'Math',)], [(u'Activity Period',), (u'ELA',)], 
                             [(u'Math',)], [(u'Student News',)]]]

        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="Peter")
        self.assertListEqual(results,expected_results)'''
        
    def test_conflicts_only(self):
        
        self.app.load(saveversion=1,student="Peter",source="56n,5s")

        expected_results = [['', u'FR', u'MO', u'TU', u'WE', u'TH'], 
                            [u'830-910', [(u'Humanities',)], [(u'Math',)], [(u'Activity Period',), (u'ELA',)], 
                             [(u'Math',)], [(u'Student News',)]]]

        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="Peter",conflicts_only="Y")
        
        for row in results:
            print row
            
        #self.assertListEqual(results,expected_results)
      
class Test_Viewer_X_Period_Y_DOW_Formats(Test_Viewer_Base):
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"test_ssloader")

    def test_Mo_830_910_Peter_adult_1attr(self):
                
        expected_results = [[dict(value='',bgcolor='#ffffff',fgcolor='#000000'), dict(value=u'MO',bgcolor='#ffffff',fgcolor='#000000')], 
                            [dict(value=u'830-910',bgcolor='#ffffff',fgcolor='#000000'), [(dict(value='ELA',bgcolor='#ffcc99',fgcolor='#ffffff'),)]]]
                            
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="Peter",formatson=True)
        
        #print results
        
        self.assertListEqual(results,expected_results)
        
    '''def test_Mo_830_910_Peter_adult_2attr(self):
                
        expected_results = [['', u'MO'], 
                            [u'830-910', [(dict(value='ELA',bgcolor='#ffcc99',fgcolor='black'),dict(value='Amelia',bgcolor='#006600',fgcolor='green'))]]]
                            
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="Peter",formatson=True)
        
        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_Peter_adult_1attr_multi_items(self):
                
        expected_results = [['', u'MO'], 
                            [u'830-910', [(dict(value='ELA',bgcolor='#ffcc99',fgcolor='black'),dict(value='Amelia',bgcolor='#006600',fgcolor='green'))]]]
                            
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="Peter",formatson=True)
        
        self.assertListEqual(results,expected_results)'''
        
class Test_Viewer_UI_Conflicts(Test_Viewer_Base):
    def setUp(self):

        files = [("prep5studentPeterPeriod1.csv",5,True,"5s"),("prep56new_Amelia_1period.csv",-1,True,"56n")]
        
        #Test_Viewer_Base.setUp(self,"test_ssloader_conflicts",files)
        Test_Viewer_Base.setUp(self,"test_ssloader_conflicts")
        
    def test_conflicts_only(self):
        
        self.app.load(saveversion=1,student="Peter",source="56n,5s")

        expected_results = [['', u'FR', u'MO', u'TU', u'WE', u'TH'], 
                            [u'830-910', '', '', u'(Activity Period)(ELA)', '', '']]


        self.app.viewer(ui=True,ztypes=['subject'],source_type="student",source_value="Peter",conflicts_only="Y")
        
        results = self.app._dumpviewergrid()
    
        self.assertListEqual(results,expected_results)
   
class Test_Viewer_UI_Conflicts_Report(Test_Viewer_Base):
    def setUp(self):

        files = [("prep5studentPeterPeriod1.csv",5,True,"5s"),("prep56new_Amelia_1period.csv",-1,True,"56n")]
        
        Test_Viewer_Base.setUp(self,"test_ssloader_conflicts",files)
        #est_Viewer_Base.setUp(self,"quad")
        
    def test_(self):
        
        self.app.load(saveversion=1,student="",source="56n,5s",unknown='N')

        expected_results = "^Peter^Jack\n830-910^(Amelia,Activity Period)(Amelia,ELA)^\n"
        
        for dow in ['TU']:
            self.app.viewer(ui=True,ztypes=['adult','subject'],source_type="adult",source_value="",yaxis_type="student",
                            constraints=[('dow',dow)],conflicts_only="Y")
        
            results = self.app._dumpviewergrid()
            
        self.assertEqual(dump2csv(results,"Y"),expected_results)     
    
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
        
        expected_results = [['', u'MO'], [u'1030-1110', u'(ELA,Aaron)(History,Issey)(Core,??)(Game Period,Dylan)(Science,Paraic)(ELA,Amelia)']]
        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        self.app.viewer(ui=True,ztypes=['subject','adult'],source_type="student",source_value="",conflicts_only='Y')

        results = self.app._dumpviewergrid()
        self.assertListEqual(results,expected_results)

    def tearDown(self):
        self.app.destroy()
    
class Test_1row_1col_1subrow_1subcol(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"1subrow_1subcol")
       
    def test_(self):
        
        expected_results = [['', u'MO'], [u'830-910', [(u'ELA',)]]]

        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")
        
        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},)]]]
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)
        
        self.assertListEqual(expected_results,results)
        
class Test_1row_1col_2subrow_1subcol(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):
        
        expected_results = [['', u'MO'],[u'830-910', [(u'ELA',), (u'Math',)]]]
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")
        
        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]]]

        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)
        
        self.assertListEqual(expected_results,results)
        
class Test_2row_1col_2subrow_1subcol(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):
        
        expected_results = [['', u'MO'], [u'830-910', [(u'ELA',), (u'Math',)]], [u'910-950', [(u'ELA',), (u'Math',)]]]


        self.app.load(saveversion=1,student="",dow="MO")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")

        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'910-950'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]]]

        self.app.load(saveversion=1,student="",dow="MO")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)

        self.assertListEqual(expected_results,results)
        
class Test_2row_2col_2subrow_1subcol(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):

        expected_results = [['', u'MO', u'TU'], 
                            [u'830-910', [(u'ELA',), (u'Math',)], [(u'ELA',), (u'Math',)]], 
                            [u'910-950', [(u'ELA',), (u'Math',)], [(u'ELA',), (u'Math',)]]]


        self.app.load(saveversion=1,student="")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")

        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'TU'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)], [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                                                                                                  ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'910-950'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)], [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                                                                                                  ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]]]
        self.app.load(saveversion=1,student="")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)
        
        self.assertListEqual(expected_results,results)
                
class Test_nrow_ncol_2subrow_1subcol(Test_Viewer_Base):
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"test_ssloader")
        
    def test_formats(self):
    
        self.app.load(saveversion=1,student="Peter",dow="MO")
    
        self.expected_result = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'??'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Karolina'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Paraic'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Issey'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'[Paraic,Rahul]'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Amelia'}], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [], [], [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'})]], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'910-950'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#666600', 'fgcolor': '#ffffff', 'value': u'Core'})], [], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'950-1030'}, [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#006600', 'fgcolor': '#ffffff', 'value': u'Science'})], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'1030-1110'}, [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ff9999', 'fgcolor': '#ffffff', 'value': u'History'})], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'1110-1210'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#663300', 'fgcolor': '#ffffff', 'value': u'Computer Time'})], [], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'1210-100'}, [], [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'??'})], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'100-140'}, [], [], [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'})]], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'140-220'}, [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ccff99', 'fgcolor': '#ffffff', 'value': u'Counseling'})], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'220-300'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ff9999', 'fgcolor': '#ffffff', 'value': u'Movement'})], [], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'300-330'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#663300', 'fgcolor': '#ffffff', 'value': u'Computer Time'})], [], [], [], [], []]]
        
        results = self.app.viewer(ui=False,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult",formatson=True)
            
        self.assertListEqual(self.expected_result,results)
        
class Test_1row_1col_2subrow_2subcol(Test_Viewer_Base):
    
    # 2 attribute displayed for each record ('subject','adult')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):
        
        expected_results = [['', u'MO'], [u'830-910', [(u'ELA', u'Amelia'), (u'Math', u'Aaron')]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="")
        
        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'}, {'bgcolor': '#006600', 'fgcolor': '#00ff00', 'value': u'Amelia'}), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'}, {'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Aaron'})]]]

        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="",formatson=True)
                
        self.assertListEqual(expected_results,results)
        
class Test_valuetype(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"1subrow_1subcol")
        
    def test_formats(self):

        expected_results = [[{'bgcolor': '#ffffff', 'valuetype': 'dow', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'valuetype': 'dow', 'fgcolor': '#000000', 'value': u'MO'}], [{'bgcolor': '#ffffff', 'valuetype': 'period', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'},)]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True,valuetype=True)
        
        print results
        
        self.assertListEqual(expected_results,results)
        
    def test_formats_3attr(self):

        expected_results = [[{'bgcolor': '#ffffff', 'valuetype': 'dow', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'valuetype': 'dow', 'fgcolor': '#000000', 'value': u'MO'}], [{'bgcolor': '#ffffff', 'valuetype': 'period', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}, {'bgcolor': '#006600', 'valuetype': 'adult', 'fgcolor': '#00ff00', 'value': u'Amelia'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'830-910'})]]]
                
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject','adult','period'],source_type="student",source_value="",formatson=True,valuetype=True)
        
        self.assertListEqual(expected_results,results)
        
class Test_Service_nopivot_1lesson(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):

        dbname='service_no_pivot_1lessons'
        refdbname='service_no_pivot_1lessons'
        
        self.database = Database(dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)

        
    def test_(self):
        
        expected_results = {'colnames': ['status', 'recordtype', 'period', 'substatus', 'source', 'session', 'adult', 'student', 'objtype', 'dow', 'userobjid', 'subject'], 'xaxis': 'row', 'yaxis': 'col'}

        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums)
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))

        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#362e37', 'valuetype': 'session', 'fgcolor': '#f2e813', 'value': u'Dylan.Game Period.Monday.1030-1110'}, {'bgcolor': '#362e37', 'valuetype': 'adult', 'fgcolor': '#f2e813', 'value': u'Dylan'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'4.1.2.37.37'}, {'bgcolor': '#d3d3d3', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Game Period'}]]


        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)
        self.assertListEqual(expected_results,results)     
        
    
class Test_Service_nopivot_2lessons(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):

        dbname='service_no_pivot_2lessons'
        refdbname='service_no_pivot_2lessons'
        
        self.database = Database(dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums)
        
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)
        
        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#006600', 'valuetype': 'session', 'fgcolor': '#00ff00', 'value': u'Amelia.ELA.Monday.100-140'}, {'bgcolor': '#006600', 'valuetype': 'adult', 'fgcolor': '#00ff00', 'value': u'Amelia'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.1.2.6.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#00ff00', 'valuetype': 'recordtype', 'fgcolor': '#ffffff', 'value': u'wp'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'140-220'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#006600', 'valuetype': 'session', 'fgcolor': '#00ff00', 'value': u'Amelia.ELA.Monday.140-220'}, {'bgcolor': '#006600', 'valuetype': 'adult', 'fgcolor': '#00ff00', 'value': u'Amelia'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'8.1.2.6.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}]]
        
        self.assertListEqual(expected_results,results)   

class Test_Service_nopivot_17lessons(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):

        dbname='service_no_pivot_17lessons'
        refdbname='service_no_pivot_17lessons'
        
        self.database = Database(dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums)
        
        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Monday.1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'4.1.9.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Tuesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jack'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TU'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.2.8.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Wednesday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.4.9.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Wednesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Orig'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.4.4.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Thursday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Bruno'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.3.3.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Thursday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.3.7.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Tuesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TU'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.2.9.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Wednesday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.4.2.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Wednesday.1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'4.4.9.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Thursday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.3.9.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Monday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Orig'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.1.4.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Thursday.220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'9.3.9.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Thursday.220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Orig'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'9.3.4.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}]]
        
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)
        
        self.assertListEqual(expected_results,results)
        
    def test_setpagelen(self):
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums,pagelen=2)
        
        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], 
                            [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Monday.1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'4.1.9.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], 
                            [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Tuesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jack'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TU'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.2.8.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}]]
             
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)

        self.assertListEqual(expected_results,results)
        
    def test_setpage(self):
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums,pagelen=2,pagenum=2)
        
        expected_results = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], 
                            [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Wednesday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.4.9.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], 
                            [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Wednesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Orig'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.4.4.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}]]
        
                     
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)

        self.assertListEqual(expected_results,results) 
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_1row_1col_1subrow_1subcol))
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_1row_1col_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_1row_1col_2subrow_2subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_2row_1col_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_2row_2col_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_nrow_ncol_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_DOW))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_DOW_Formats))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_Adult))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_UI))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_valuetype))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Service_nopivot_1lesson))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Service_nopivot_2lessons))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Service_nopivot_17lessons))'''
    
    
    ''' only need these if conflicts code is uncommented in viewer '''
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_UI_Conflicts))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_UI_Conflicts_Report))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Conflicts_master_record))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Conflicts))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


