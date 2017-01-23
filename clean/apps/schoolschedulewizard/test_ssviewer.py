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
from shutil import copyfile
from copy import deepcopy


def create_test_db(dbname,files,keepversion):
    #filename,prep):
    #database = Database(dbname)
    #files = [(filename,prep,True)]
    ssloader = SSLoader(dbname)
    ssloader.keepversion = keepversion
    ssloader.run(dbname,files)
    
class Test_Viewer_Base(unittest.TestCase):
    
    def setUp(self,dbname,files=None,keepversion=False):
        
        self.dbname = dbname
        
        if files <> None:
            create_test_db(self.dbname,files,keepversion)
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

'''
if the tests fail because there are no pm periods; its because the tests are still
expecting the old style periods; fire up dbtblviewer and update the periods to
1210-100,100-140,140-220,220-300,300-330 and rerun the test_ abovwe
'''


class Test_Viewer_X_Student_Y_Subject(Test_Viewer_Base):
    
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssloader","prep5student.csv",5,True)
        Test_Viewer_Base.setUp(self,"test_ssloader")

    def test_Peter_Stan_subject(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Peter'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Math'}, [({'value': u'TH'}, {'value': u'1210-100'}), 
                                                                                                ({'value': u'TU'}, {'value': u'1210-100'}), 
                                                                                                ({'value': u'TH'}, {'value': u'1030-1110'}), 
                                                                                                ({'value': u'TU'}, {'value': u'1030-1110'})]]]       
                
        self.app.load(saveversion=1,student="Peter",teacher="Stan")

        results = self.app.viewer(ui=False,ztypes=['dow','period'],source_type="student",source_value="Peter",
                                  yaxis_type="student",xaxis_type="subject")

        self.assertListEqual(results,expected_results)
        
    def test_Peter_Stan_subject_count(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Peter'}], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Math'}, [({'value': 4},)]]]
                
        self.app.load(saveversion=1,student="Peter",teacher="Stan")

        results = self.app.viewer(ui=False,ztypes=['*'],source_type="student",source_value="Peter",
                                  yaxis_type="student",xaxis_type="subject")

        self.assertListEqual(results,expected_results)
        
    def test_inverse(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Math'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Peter'}, [({'value': u'TH'}, {'value': u'1210-100'}), ({'value': u'TU'}, {'value': u'1210-100'}), ({'value': u'TH'}, {'value': u'1030-1110'}), ({'value': u'TU'}, {'value': u'1030-1110'})]]]
                
        self.app.load(saveversion=1,student="Peter",teacher="Stan")

        results = self.app.viewer(ui=False,ztypes=['dow','period'],source_type="student",source_value="Peter",
                                  yaxis_type="subject",xaxis_type="student")
        
        self.assertListEqual(results,expected_results)
        
        
class Test_Viewer_X_Subject_Y_Adult(Test_Viewer_Base):

    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        # simple case as subject index is not used in a period / dow pivot        
        expected_results = [['', u'??', u'Amelia'], 
                            [u'Math', [(u'MO', u'830-910')], []], 
                            [u'??', [(u'WE', u'830-910')], []], 
                            [u'Student News', [(u'TH', u'830-910')], []], 
                            [u'Humanities', [(u'FR', u'830-910')], [(u'TU', u'910-950')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='adult',xaxis_type='subject',
                    source_type='student',source_value='Clayton',
                    ztypes=['dow','period'])
                  
        result = ssviewer_utils.dataset_pivot(**args)   
        
        self.assertListEqual(result,expected_results)

    def test_inverse(self):
        
        # simple case as subject index is not used in a period / dow pivot
        
        expected_results = [['', u'Math', u'??', u'Student News', u'Humanities'], 
                            [u'??', [(u'MO', u'830-910')], [(u'WE', u'830-910')], [(u'TH', u'830-910')], [(u'FR', u'830-910')]], 
                            [u'Amelia', [], [], [], [(u'TU', u'910-950')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='subject',xaxis_type='adult',
                    source_type='student',source_value='Clayton',
                    ztypes=['dow','period'])
                  
        result = ssviewer_utils.dataset_pivot(**args)   

        self.assertListEqual(result,expected_results)
        
    def tearDown(self):
        copyfile(self.dbname+".sqlite.backup",self.dbname+".sqlite")
        
class Test_Viewer_Adult_X_Student_Y_Recordtype(Test_Viewer_Base):

    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        # simple case as subject index is not used in a period / dow pivot        
        expected_results = [['', u'Clayton'], [u'wp', [(u'TU', u'910-950')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='student',xaxis_type='recordtype',
                    source_type='adult',source_value='Amelia',
                    ztypes=['dow','period'])
                
        result = ssviewer_utils.dataset_pivot(**args)   

        self.assertListEqual(result,expected_results)

    def test_inverse(self):
        
        # simple case as subject index is not used in a period / dow pivot
        
        expected_results = [['', u'wp'], [u'Clayton', [(u'TU', u'910-950')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='recordtype',xaxis_type='student',
                    source_type='adult',source_value='Amelia',
                    ztypes=['dow','period'])
                  
        result = ssviewer_utils.dataset_pivot(**args)   

        self.assertListEqual(result,expected_results)
        
    def tearDown(self):
        copyfile(self.dbname+".sqlite.backup",self.dbname+".sqlite")
        
        
class Test_Viewer_Subject_X_Student_Y_Recordtype(Test_Viewer_Base):

    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        # simple case as subject index is not used in a period / dow pivot        
        expected_results =  [['', u'Clayton'], 
                             [u'wp', [(u'TU', u'910-950')]], 
                             ['academic', [(u'FR', u'830-910')]]]
        
                
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='student',xaxis_type='recordtype',
                    source_type='subject',source_value='Humanities',
                    ztypes=['dow','period'])
             
        result = ssviewer_utils.dataset_pivot(**args)     

        self.assertListEqual(result,expected_results)

    def test_inverse(self):
        
        # simple case as subject index is not used in a period / dow pivot
        
        expected_results = [['', u'wp', 'academic'], 
                            [u'Clayton', [(u'TU', u'910-950')], [(u'FR', u'830-910')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='recordtype',xaxis_type='student',
                    source_type='subject',source_value='Humanities',
                    ztypes=['dow','period'])
                  
        result = ssviewer_utils.dataset_pivot(**args)   
        
        self.assertListEqual(result,expected_results)
        
    def tearDown(self):
        copyfile(self.dbname+".sqlite.backup",self.dbname+".sqlite")
   
class Test_Viewer_All_X_Period_Y_DOW(Test_Viewer_Base):

    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        # simple case as subject index is not used in a period / dow pivot
        expected_results = [['', u'830-910', u'910-950'], 
                            [u'MO', [(u'Math', u'??')], []], 
                            [u'WE', [(u'??',)], []], 
                            [u'TH', [(u'Student News', u'??')], []], 
                            [u'TU', [], [(u'Humanities', u'Amelia')]], 
                            [u'FR', [(u'Humanities', u'??')], []]]
        
                
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='period',xaxis_type='dow',
                    source_type='student',source_value='',
                    ztypes=['subject','adult'])
                  
        result = ssviewer_utils.dataset_pivot(**args)  
        
        self.assertListEqual(result,expected_results)

        
class Test_Viewer_All_X_Period_Y_DOW_Constraints(Test_Viewer_Base):

    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        # simple case as subject index is not used in a period / dow pivot
        expected_results = [['', u'830-910'], 
                            [u'WE', [(u'??',)]]]
        
                
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='period',xaxis_type='dow',
                    source_type='student',source_value='',
                    ztypes=['subject','adult'],constraints=[['dow','WE'],['period','830-910']])
                  
        result = ssviewer_utils.dataset_pivot(**args)   

        self.assertListEqual(result,expected_results)

        
class Test_Viewer_X_Student_Y_Recordtype(Test_Viewer_Base):

    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        # simple case as subject index is not used in a period / dow pivot
        expected_results = [['', u'Clayton'], 
                            [u'wp', [(u'MO', u'830-910'), (u'WE', u'830-910'), (u'TU', u'910-950')]], 
                            ['academic', [(u'TH', u'830-910'), (u'FR', u'830-910')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='student',xaxis_type='recordtype',
                    source_type='student',source_value='Clayton',
                    ztypes=['dow','period'])
                  
        result = ssviewer_utils.dataset_pivot(**args)   

        self.assertListEqual(result,expected_results)
        
        
    def test_ztypes_subject_adult(self):
        
        # simple case as subject index is not used in a period / dow pivot
        expected_results = [['', u'Clayton'], 
                            [u'wp', [(u'MO', u'830-910'), (u'WE', u'830-910'), (u'TU', u'910-950')]], 
                            ['academic', [(u'TH', u'830-910'), (u'FR', u'830-910')]]]
        
        expected_results = [['', u'Clayton'], 
                            [u'wp', [(u'Math', u'??'), (u'??',), (u'Humanities', u'Amelia')]], 
                            ['academic', [(u'Student News', u'??'), (u'Humanities', u'??')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='student',xaxis_type='recordtype',
                    source_type='student',source_value='Clayton',
                    ztypes=['subject','adult'])
                  
        result = ssviewer_utils.dataset_pivot(**args)   
        
        self.assertListEqual(result,expected_results)

    def test_inverse(self):
        
        # simple case as subject index is not used in a period / dow pivot
        
        expected_results = [['', u'wp', 'academic'], 
                            [u'Clayton', [(u'MO', u'830-910'), (u'WE', u'830-910'), (u'TU', u'910-950')], [(u'TH', u'830-910'), (u'FR', u'830-910')]]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='recordtype',xaxis_type='student',
                    source_type='student',source_value='Clayton',
                    ztypes=['dow','period'])
                  
        result = ssviewer_utils.dataset_pivot(**args)   
        
        self.assertListEqual(result,expected_results)
        
    def tearDown(self):
        copyfile(self.dbname+".sqlite.backup",self.dbname+".sqlite")
        

class Test_Viewer_X_Period_Y_DOW(Test_Viewer_Base):
    
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssloader",[("prep5student.csv",5,True)])
        Test_Viewer_Base.setUp(self,"test_ssloader")
    
    #def test_(self):
    #    pass
    
    def test_Mo_830_910_Peter_adult_subject(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'value': u'Amelia'}, {'value': u'ELA'})]]]
        
        
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['adult','subject'],source_type="student",source_value="Peter")
    
    
        self.assertListEqual(results,expected_results)

    
    def test_Mo_Peter_adult_subject(self):

        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1210-100'}, [({'value': u'[Paraic,Rahul]'}, {'value': u'??'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1030-1110'}, [({'value': u'Issey'}, {'value': u'History'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'value': u'Amelia'}, {'value': u'ELA'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1110-1210'}, [({'value': u'??'}, {'value': u'Computer Time'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'950-1030'}, [({'value': u'Paraic'}, {'value': u'Science'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'300-330'}, [({'value': u'??'}, {'value': u'Computer Time'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'100-140'}, [({'value': u'Amelia'}, {'value': u'ELA'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'910-950'}, [({'value': u'??'}, {'value': u'Core'})]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'220-300'}, [({'value': u'??'}, {'value': u'Movement'})]],
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'140-220'}, [({'value': u'Karolina'}, {'value': u'Counseling'})]]]
        self.app.load(saveversion=1,student="Peter",dow="MO")

        results = self.app.viewer(ui=False,ztypes=['adult','subject'],source_type="student",source_value="Peter")
        
        self.assertListEqual(results,expected_results)
    
    def test_Mo_830_910_Peter_adult_recordtype(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1030-1110'}, [({'value': u'Issey'}, {'value': u'wp'})]]]
        
        self.app.load(saveversion=1,student="Peter",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['adult','recordtype'],source_type="student",source_value="Peter")

        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_adult_subject(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1030-1110'}, [({'value': u'Jake'}, {'value': u'Aaron'}), ({'value': u'Peter'}, {'value': u'Issey'}), ({'value': u'Orig'}, {'value': u'??'}), ({'value': u'Bruno'}, {'value': u'Dylan'}), ({'value': u'Oscar'}, {'value': u'Paraic'}), ({'value': u'Clayton'}, {'value': u'Dylan'}), ({'value': u'Jack'}, {'value': u'Paraic'}), ({'value': u'Nathaniel'}, {'value': u'Amelia'}), ({'value': u'Stephen'}, {'value': u'??'})]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['student','adult'],source_type="student",source_value="")
        
        #self.app.mainloop()
        
        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_count_groupby(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
         [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1030-1110'}, [({'value': 9},)]]]

        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110")

        results = self.app.viewer(ui=False,ztypes=['*'],source_type="student",source_value="")

        self.assertListEqual(results,expected_results)
               
    def test_Mo_830_910_adult_subject_no_unknowns(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1030-1110'}, [({'value': u'Jake'}, {'value': u'Aaron'}), ({'value': u'Peter'}, {'value': u'Issey'}), ({'value': u'Bruno'}, {'value': u'Dylan'}), ({'value': u'Oscar'}, {'value': u'Paraic'}), ({'value': u'Clayton'}, {'value': u'Dylan'}), ({'value': u'Jack'}, {'value': u'Paraic'}), ({'value': u'Nathaniel'}, {'value': u'Amelia'})]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="1030-1110",unknown='N')

        results = self.app.viewer(ui=False,ztypes=['student','adult'],source_type="student",source_value="")
        
        self.assertListEqual(results,expected_results)
    
class Test_Viewer_X_Period_Y_Adult(Test_Viewer_Base):
    
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssloader","prep5student.csv",5,True)
        Test_Viewer_Base.setUp(self,"test_ssloader")

    def test_Karolina_Peter_adult_subject(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Karolina'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'140-220'}, [({'value': u'Peter'}, {'value': u'Counseling'})]]]
        
        self.app.load(saveversion=1,student="Peter",teacher="Karolina")

        results = self.app.viewer(ui=False,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult")
        
        self.assertListEqual(results,expected_results)
        
    def test_830_910_Peter_adult_subject(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'[Paraic,Rahul]'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Issey'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Amelia'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'??'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Paraic'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Karolina'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1210-100'}, [({'value': u'Peter'}, {'value': u'??'})], [], [], [({'value': u'Peter'}, {'value': u'??'})], [], []], # because of how indexing works a phantom entry is created where adult=??; this is due to a conflict when ?? gets used for adult and subject
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1030-1110'}, [], [({'value': u'Peter'}, {'value': u'History'})], [], [], [], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [], [], [({'value': u'Peter'}, {'value': u'ELA'})], [], [], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1110-1210'}, [], [], [], [({'value': u'Peter'}, {'value': u'Computer Time'})], [], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'950-1030'}, [], [], [], [], [({'value': u'Peter'}, {'value': u'Science'})], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'300-330'}, [], [], [], [({'value': u'Peter'}, {'value': u'Computer Time'})], [], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'100-140'}, [], [], [({'value': u'Peter'}, {'value': u'ELA'})], [], [], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'910-950'}, [], [], [], [({'value': u'Peter'}, {'value': u'Core'})], [], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'220-300'}, [], [], [], [({'value': u'Peter'}, {'value': u'Movement'})], [], []], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'140-220'}, [], [], [], [], [], [({'value': u'Peter'}, {'value': u'Counseling'})]]]
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
                
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},)]]]
        
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="Peter",formatson=True)

        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_Peter_adult_2attr(self):
                
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'}, {'bgcolor': u'#006600', 'fgcolor': u'#00ff00', 'value': u'Amelia'})]]]
                            
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="Peter",formatson=True)
        
        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_Peter_adult_1attr_multi_items(self):
                              
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'}, {'bgcolor': u'#006600', 'fgcolor': u'#00ff00', 'value': u'Amelia'})]]]
       
        self.app.load(saveversion=1,student="Peter",dow="MO",period="830-910")

        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="Peter",formatson=True)
        
        self.assertListEqual(results,expected_results)
        
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
        
        expected_results = [['', u'[Paraic,Rahul]', u'Issey', u'Amelia', u'??', u'Paraic', u'Karolina'], 
                            [u'1210-100', u'(Peter,??)', '', '', u'(Peter,??)', '', ''], # because of how the indexing works; a  phantom cell is created for adult=?? 
                            [u'1030-1110', '', u'(Peter,History)', '', '', '', ''], 
                            [u'830-910', '', '', u'(Peter,ELA)', '', '', ''], 
                            [u'1110-1210', '', '', '', u'(Peter,Computer Time)', '', ''], 
                            [u'950-1030', '', '', '', '', u'(Peter,Science)', ''], 
                            [u'300-330', '', '', '', u'(Peter,Computer Time)', '', ''], 
                            [u'100-140', '', '', u'(Peter,ELA)', '', '', ''], 
                            [u'910-950', '', '', '', u'(Peter,Core)', '', ''], 
                            [u'220-300', '', '', '', u'(Peter,Movement)', '', ''], 
                            [u'140-220', '', '', '', '', '', u'(Peter,Counseling)']]
        
        self.app.load(saveversion=1,student="Peter",dow="MO")

        self.app.viewer(ui=True,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult")

        #self.app.mainloop()
        
        results = self.app._dumpviewergrid()

        self.assertListEqual(results,expected_results)
        
    def test_Mo_830_910_count_groupby(self):
        
        expected_results = [['', u'MO'], [u'1030-1110', '9']]

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
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'value': u'ELA'},)]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")
        
        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},)]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)
        
        self.assertListEqual(expected_results,results)
        
class Test_1row_1col_2subrow_1subcol(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
         [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, 
          [({'value': u'ELA'},), ({'value': u'Math'},)]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")
        
        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},), 
                                                                                                   ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'},)]]]

        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)
        
        self.assertListEqual(expected_results,results)
        
class Test_2row_1col_2subrow_1subcol(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'value': u'ELA'},), ({'value': u'Math'},)]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'910-950'}, [({'value': u'ELA'},), ({'value': u'Math'},)]]]
        

        self.app.load(saveversion=1,student="",dow="MO")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")

        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},), 
                                                                                                   ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'},)]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'910-950'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},), 
                                                                                                   ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'},)]]]
        
        self.app.load(saveversion=1,student="",dow="MO")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)

        self.assertListEqual(expected_results,results)
        
class Test_2row_2col_2subrow_1subcol(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):
        expected_result = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'TU'}], 
                           [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'value': u'ELA'},), ({'value': u'Math'},)], [({'value': u'ELA'},), ({'value': u'Math'},)]], 
                           [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'910-950'}, [({'value': u'ELA'},), ({'value': u'Math'},)], [({'value': u'ELA'},), ({'value': u'Math'},)]]]


        self.app.load(saveversion=1,student="")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="")

        self.assertListEqual(expected_result,results)
        
    def test_formats(self):

                                     
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'TU'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},), 
                                                                                                   ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'},)], [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},), 
                                                                                                                                                                          ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'},)]], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'910-950'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},), 
                                                                                                   ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'},)], [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'},), 
                                                                                                                                                                          ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'},)]]]                                                                                                                                                                                                              
        
        self.app.load(saveversion=1,student="")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True)
        
        self.assertListEqual(expected_results,results)
                
class Test_nrow_ncol_2subrow_1subcol(Test_Viewer_Base):
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"test_ssloader")
        
    '''def test_(self):
        pass'''
    
    def test_formats(self):
    
        self.app.load(saveversion=1,student="Peter",dow="MO")

        #self.app.mainloop()
        self.expected_result = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'[Paraic,Rahul]'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Issey'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Amelia'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'??'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Paraic'}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'Karolina'}], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1210-100'}, [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'??'})], [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'??'})], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1030-1110'}, [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#ff9999', 'fgcolor': u'#000000', 'value': u'History'})], [], [], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'})], [], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'1110-1210'}, [], [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#663300', 'fgcolor': u'#000000', 'value': u'Computer Time'})], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'950-1030'}, [], [], [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#006600', 'fgcolor': u'#000000', 'value': u'Science'})], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'300-330'}, [], [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#663300', 'fgcolor': u'#000000', 'value': u'Computer Time'})], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'100-140'}, [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'})], [], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'910-950'}, [], [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#666600', 'fgcolor': u'#000000', 'value': u'Core'})], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'220-300'}, [], [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#ff9999', 'fgcolor': u'#000000', 'value': u'Movement'})], [], []], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'140-220'}, [], [], [], [], [], [({'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#ccff99', 'fgcolor': u'#000000', 'value': u'Counseling'})]]]
        
        results = self.app.viewer(ui=False,ztypes=['student','subject'],source_type="student",source_value="Peter",yaxis_type="adult",formatson=True)
        
        self.assertListEqual(self.expected_result,results)
        
class Test_1row_1col_2subrow_2subcol(Test_Viewer_Base):
    
    # 2 attribute displayed for each record ('subject','adult')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"2subrow_1subcol")
       
    def test_(self):
        
        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], 
                            [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'value': u'ELA'}, {'value': u'Amelia'}), ({'value': u'Math'}, {'value': u'Aaron'})]]]
        
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="")
        
        self.assertListEqual(expected_results,results)
        
    def test_formats(self):

        expected_results = [[{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'MO'}], [{'bgcolor': u'#ffffff', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'fgcolor': u'#000000', 'value': u'ELA'}, {'bgcolor': u'#006600', 'fgcolor': u'#00ff00', 'value': u'Amelia'}), ({'bgcolor': u'#99ffcc', 'fgcolor': u'#000000', 'value': u'Math'}, {'bgcolor': u'#d3d3d3', 'fgcolor': u'#ffffff', 'value': u'Aaron'})]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject','adult'],source_type="student",source_value="",formatson=True)
                
        self.assertListEqual(expected_results,results)
        
class Test_valuetype(Test_Viewer_Base):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"1subrow_1subcol")
        
    def test_formats(self):

        expected_results = [[{'bgcolor': u'#ffffff', 'valuetype': 'dow', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'valuetype': 'dow', 'fgcolor': u'#000000', 'value': u'MO'}], [{'bgcolor': u'#ffffff', 'valuetype': 'period', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'},)]]]
        
        self.app.load(saveversion=1,student="",dow="MO",period="830-910")
        
        results = self.app.viewer(ui=False,ztypes=['subject'],source_type="student",source_value="",formatson=True,valuetype=True)
        
        self.assertListEqual(expected_results,results)
        
    def test_formats_3attr(self):

        expected_results = [[{'bgcolor': u'#ffffff', 'valuetype': 'dow', 'fgcolor': u'#000000', 'value': ''}, {'bgcolor': u'#ffffff', 'valuetype': 'dow', 'fgcolor': u'#000000', 'value': u'MO'}], [{'bgcolor': u'#ffffff', 'valuetype': 'period', 'fgcolor': u'#000000', 'value': u'830-910'}, [({'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'}, {'bgcolor': u'#006600', 'valuetype': 'adult', 'fgcolor': u'#00ff00', 'value': u'Amelia'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'830-910'})]]]
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
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums)
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))

        expected_results = [[{'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'status'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'substatus'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'recordtype'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'period'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'dow'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'source'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'session'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'adult'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'student'},
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'id'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'objtype'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'prep'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'userobjid'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'subject'}], 
                            
                            [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'1030-1110'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'MO'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, 
                             {'bgcolor': u'#362e37', 'valuetype': 'session', 'fgcolor': u'#f2e813', 'value': u'Dylan.Game Period.Monday.1030-1110'}, 
                             {'bgcolor': u'#362e37', 'valuetype': 'adult', 'fgcolor': u'#f2e813', 'value': u'Dylan'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Clayton'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'00427CB0'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'4.1.2.37.37'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'subject', 'fgcolor': u'#ffffff', 'value': u'Game Period'}]]


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
        
        expected_results = [[{'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'status'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'substatus'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'recordtype'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'period'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'dow'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'source'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'session'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'adult'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'student'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'id'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'objtype'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'prep'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'userobjid'}, 
                             {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'subject'}], 
                            [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'100-140'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'MO'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, 
                             {'bgcolor': u'#006600', 'valuetype': 'session', 'fgcolor': u'#00ff00', 'value': u'Amelia.ELA.Monday.100-140'}, 
                             {'bgcolor': u'#006600', 'valuetype': 'adult', 'fgcolor': u'#00ff00', 'value': u'Amelia'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Clayton'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'004ACB88'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'7.1.2.6.1'}, 
                             {'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'}], 
                            [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, 
                             {'bgcolor': u'#00ff00', 'valuetype': 'recordtype', 'fgcolor': u'#000000', 'value': u'wp'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'140-220'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'MO'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, 
                             {'bgcolor': u'#006600', 'valuetype': 'session', 'fgcolor': u'#00ff00', 'value': u'Amelia.ELA.Monday.140-220'}, 
                             {'bgcolor': u'#006600', 'valuetype': 'adult', 'fgcolor': u'#00ff00', 'value': u'Amelia'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Clayton'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'3379671'}, 
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'},
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5},
                             {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'8.1.2.6.1'}, 
                             {'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'}]]
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
        
        expected_results = [[{'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'status'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'substatus'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'recordtype'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'period'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'dow'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'source'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'session'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'adult'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'student'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'id'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'objtype'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'prep'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'userobjid'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'subject'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'1030-1110'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'MO'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.ELA.Monday.1030-1110'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Jake'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'019C3483'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'4.1.9.1.1'}, {'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'TU'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Activity Period.Tuesday.100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Jack'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'058808F5'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'7.2.8.1.9'}, {'bgcolor': u'#cccc00', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'Activity Period'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'WE'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Student News.Wednesday.950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Jake'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'0475D8EF'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'3.4.9.1.5'}, {'bgcolor': u'#003333', 'valuetype': 'subject', 'fgcolor': u'#ffff99', 'value': u'Student News'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'WE'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.ELA.Wednesday.100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Orig'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'029EE113'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'7.4.4.1.1'}, {'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'TH'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Student News.Thursday.950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Bruno'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'01C1A403'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'3.3.3.1.5'}, {'bgcolor': u'#003333', 'valuetype': 'subject', 'fgcolor': u'#ffff99', 'value': u'Student News'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'TH'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Student News.Thursday.950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Peter'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'014381EB'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'3.3.7.1.5'}, {'bgcolor': u'#003333', 'valuetype': 'subject', 'fgcolor': u'#ffff99', 'value': u'Student News'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'TU'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Activity Period.Tuesday.100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Jake'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'00A5CC47'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'7.2.9.1.9'}, {'bgcolor': u'#cccc00', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'Activity Period'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'WE'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Student News.Wednesday.950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Clayton'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'4868523'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'3.4.2.1.5'}, {'bgcolor': u'#003333', 'valuetype': 'subject', 'fgcolor': u'#ffff99', 'value': u'Student News'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'1030-1110'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'WE'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.ELA.Wednesday.1030-1110'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Jake'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'0564B672'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'4.4.9.1.1'}, {'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'TH'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Activity Period.Thursday.950-1030'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Jake'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'1973804'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'3.3.9.1.9'}, {'bgcolor': u'#cccc00', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'Activity Period'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'MO'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.ELA.Monday.100-140'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Orig'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'02363A8B'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'7.1.4.1.1'}, {'bgcolor': u'#ffcc99', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'ELA'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'220-300'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'TH'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Activity Period.Thursday.220-300'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Jake'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'022AAB36'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'9.3.9.1.9'}, {'bgcolor': u'#cccc00', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'Activity Period'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'master'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'complete'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'recordtype', 'fgcolor': u'#ffffff', 'value': 'academic'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'period', 'fgcolor': u'#ffffff', 'value': u'220-300'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'dow', 'fgcolor': u'#ffffff', 'value': u'TH'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'source', 'fgcolor': u'#ffffff', 'value': u'dbinsert'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'session', 'fgcolor': u'#ffffff', 'value': u'Aaron.Activity Period.Thursday.220-300'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'adult', 'fgcolor': u'#ffffff', 'value': u'Aaron'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'student', 'fgcolor': u'#ffffff', 'value': u'Orig'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'id', 'fgcolor': u'#ffffff', 'value': u'04F4C865'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'objtype', 'fgcolor': u'#ffffff', 'value': 'lesson'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'prep', 'fgcolor': u'#ffffff', 'value': 5}, {'bgcolor': u'#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': u'#ffffff', 'value': u'9.3.4.1.9'}, {'bgcolor': u'#cccc00', 'valuetype': 'subject', 'fgcolor': u'#000000', 'value': u'Activity Period'}]]
        
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)
        
        self.assertListEqual(expected_results,results)
        
    def test_setpagelen(self):
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums,pagelen=2,columns=['subject','student'])
             
        expected_results = [[{'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'status'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'substatus'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'recordtype'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'period'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'dow'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'source'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'session'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'adult'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'student'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'id'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'objtype'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'prep'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'userobjid'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'subject'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'ELA'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'Jake'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'Activity Period'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'Jack'}]]
        
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)
        
        self.assertListEqual(expected_results,results)
        
    def test_setpage(self):
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums)
        
        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums,pagelen=2,pagenum=2,columns=['subject','student'])
        
        expected_results = [[{'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'status'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'substatus'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'recordtype'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'period'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'dow'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'source'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'session'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'adult'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'student'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'id'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'objtype'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'prep'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'userobjid'}, {'bgcolor': u'#ffffff', 'valuetype': 'col', 'fgcolor': u'#000000', 'value': 'subject'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'Student News'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'Jake'}], [{'bgcolor': u'#ffffff', 'valuetype': 'row', 'fgcolor': u'#000000', 'value': u'ELA'}, {'bgcolor': u'#d3d3d3', 'valuetype': 'substatus', 'fgcolor': u'#ffffff', 'value': u'Orig'}]]
                     
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        results = ssviewer_utils.dataset_serialize(grid,formatson=True,schema=schema)

        self.assertListEqual(expected_results,results) 
        
class Test_Viewer_Update_and_Pivot(Test_Viewer_Base):
    
    '''
    cp test_ssloader.sqlite to test_ssviewer_update.sqlite
    to make sure has recordtype table and that it has old periods
    uncomment the setUp with files and just un comment pass  
    then run again with inverse
    '''
    
    ''' 
    tests that updates are reflected correctly in the index
    '''
    
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_update_period_view_period_pivot(self):
    
        # tricky case as the index needs to be updated to reflect the change
        
        expected_results = [['', u'MO', u'WE', u'TH', u'TU', u'FR'], 
                            [u'830-910', [], [(u'??',)], [(u'Student News',)], [], [(u'Humanities',)]], 
                            [u'910-950', [(u'Math',)], [], [], [(u'Humanities',)], []]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                            self.of,self.enums,unknown='Y')
        
        lesson = self.of.object_get('lesson','1.1.2.8.4')
        lesson.keepversion=True
        lesson.customtimestamp = "%y%m%d_%H%M%S"

        ssviewer_utils._lesson_change(lesson,delete=True)
        
        lesson.update(self.of,'period',"910-950")
        ssviewer_utils._lesson_change(lesson)
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='dow',xaxis_type='period',
                    source_type='student',source_value='Clayton',
                    ztypes=['subject'])
    
        result = ssviewer_utils.dataset_pivot(**args)   

        self.assertListEqual(result,expected_results)
        
    def test_update_subject_view_period_pivot(self):
        
        # simple case as subject index is not used in a period / dow pivot
        
        expected_results = [['', u'MO', u'WE', u'TH', u'TU', u'FR'], 
                            [u'830-910', [(u'Humanities',)], [(u'??',)], [(u'Student News',)], [], [(u'Humanities',)]], 
                            [u'910-950', [], [], [], [(u'Humanities',)], []]]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='dow',xaxis_type='period',
                    source_type='student',source_value='Clayton',
                    ztypes=['subject'])
        
        lesson = self.of.object_get('lesson','1.1.2.8.4')
        lesson.keepversion=True
        lesson.customtimestamp = "%y%m%d_%H%M%S"
        _newid = lesson.update(self.of,'subject',"Humanities")
                  
        result = ssviewer_utils.dataset_pivot(**args)   

        self.assertListEqual(result,expected_results)
        
    def tearDown(self):
        copyfile(self.dbname+".sqlite.backup",self.dbname+".sqlite")
        
        
class Test_Viewer_Update(Test_Viewer_Base):
    
    '''
    cp test_ssloader.sqlite to test_ssviewer_update.sqlite
    to make sure has recordtype table and that it has old periods
    
    uncomment the setUp with files and just un comment pass
    
    then run again with inverse
    '''
    def setUp(self):
        #Test_Viewer_Base.setUp(self,"test_ssviewer_update",[("prep5studentClaytonPeriod1WP.csv",5,True)],True)
        Test_Viewer_Base.setUp(self,"test_ssviewer_update")
        
        self.dbname='test_ssviewer_update'
        refdbname='test_ssviewer_update'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
        
    def test_object_updates(self):
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        lesson = self.of.object_get('lesson','1.1.2.8.4')
        lesson.keepversion=True
        lesson.customtimestamp = "%y%m%d_%H%M%S"
        _newid = lesson.update(self.of,'period',"910-950")
                    
        expected_results = {'status': u'master', 'substatus': u'incomplete', 'recordtype': u'wp', 
                            'period': u'830-910', 'dow': u'MO', 'source': u'dbinsert', 
                            'session': u'??.Math.Monday.830-910', 'adult': u'??', 'student': u'Clayton', 
                            'id': u'046CE5DA', 'objtype': 'lesson', 'prep': 5, 'userobjid': u'1.1.2.8.4', 
                            'subject': u'foobar'}
        
        # just test keys as order changes
        _dmkeys = lesson.dm.keys()
        _expkeys = expected_results.keys()
        _dmkeys.sort()
        _expkeys.sort()
        
        self.assertEqual(_dmkeys,_expkeys)
        
        # test specific value has been updated
        self.assertEqual(lesson.dm['period'],"910-950")
        self.assertEqual(getattr(lesson,'period').name,"910-950")
        
        # test that the period object values have not been changed
        oldval = self.of.object_get_byval("period","830-910")
        newval = self.of.object_get_byval("period","910-950")
        self.assertEquals(oldval.name,"830-910")
        self.assertEquals(newval.name,"910-950")
        
        # test that the period attr on lesson now points to the 910-950 period
        self.assertEquals(getattr(lesson,'period'),newval)
        
        # test that the id in dm has been updated
        self.assertEqual(_newid,lesson.dm['id'])
        
        # test that the id in on the object has been updated
        self.assertEqual(lesson.id.name,_newid)
        
    '''def test_(self):
        pass'''
        
    '''def test_create_versions(self):

        expected_results = [['Math'],['Math'],['Math'],['Math'],['Math']]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y')
        
        
        for lesson in self.of.query('lesson'):
            lesson.keepversion=True
            lesson.customtimestamp = "%y%m%d_%H%M%S"
            lesson.update(self.of,'subject',"Math")
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"lesson",['subject'],
                                    [['__version','=',"\"current\""],
                                     ['status','=',"\"master\""]])
        
        self.assertListEqual(expected_results,rows)'''
        
    def tearDown(self):
        copyfile(self.dbname+".sqlite.backup",self.dbname+".sqlite")

class Test_Viewer_Update_Recover(Test_Viewer_Base):
    
    def setUp(self):
        Test_Viewer_Base.setUp(self,"test_ssviewer_update_recover")
        
        self.dbname='test_ssviewer_update_recover'
        refdbname='test_ssviewer_update_recover'
        
        self.database = Database(self.dbname)
        self.refdatabase = Database(refdbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.refdatabase)
        
    def test_(self):
        
        expected_results = [['foobar'],['foobar'],['foobar'],['foobar'],['foobar']]
        
        ssviewer_utils.dataset_load(self.database,self.refdatabase,
                                    self.of,self.enums,unknown='Y',
                                    keepversion=True)
        
        results = []
        for lesson in self.of.query('lesson'):
            results.append([lesson.subject.name])
            
        self.assertListEqual(expected_results,results)
        
    
    def tearDown(self):
        copyfile(self.dbname+".sqlite.backup",self.dbname+".sqlite")
        
class Test_Viewer_Service(Test_Viewer_Base):
    pass

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    # Testing pivots
    
    # Student pivot default axes (period/dow)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_1row_1col_1subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_1row_1col_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_1row_1col_2subrow_2subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_2row_1col_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_2row_2col_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_nrow_ncol_2subrow_1subcol))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_DOW))
    
    # Student pivot different axes
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Student_Y_Subject))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_Adult))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Subject_Y_Adult))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Student_Y_Recordtype))
   
    # Different objtype pivot with different axes
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Adult_X_Student_Y_Recordtype))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Subject_X_Student_Y_Recordtype)) 
    
    # source_value == all
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_All_X_Period_Y_DOW))
    
    # constraints
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_All_X_Period_Y_DOW_Constraints))
    
    # Misc
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_UI))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_X_Period_Y_DOW_Formats))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_valuetype))

    # Testing updates
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Update))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Update_Recover))
    
    # Testing updates and pivots
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Update_and_Pivot))
    
    # Test lists (no pivots)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Service_nopivot_1lesson))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Service_nopivot_2lessons))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Service_nopivot_17lessons))
    
    #only need these if conflicts code is uncommented in viewer
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_UI_Conflicts))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_UI_Conflicts_Report))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Conflicts_master_record))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Viewer_Conflicts))'''
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


