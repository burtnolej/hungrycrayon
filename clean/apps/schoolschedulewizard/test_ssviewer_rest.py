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
        ssrest.restquery(self.url + "command/reload",unknown="Y")
        
    def _queryxml(self,buf,xpathstr,tag):
        tree_element = xmltree.fromstring(buf)
        xmlroot = ElementTree.ElementTree(tree_element) 
        return(xmlroot.findall(xpathstr))
    
    def _getelementstext(self,elements):
        return [element.find('value').text for element in elements]  
    
    def _parsedmdump(self,xml,field):
        # if field equal to id result will be [[#id,#subject,dm=#id]]
        # if there is only one record and subject,id is requested
        
        tree_element = xmltree.fromstring(xml)
        xmlroot = ElementTree.ElementTree(tree_element) 

        dm = []
        for xmlrow in xmlroot.findall(".//tr"):
            _dm = []
            for xmlcell in xmlrow.findall(".//td")[1:-1]: # skip 1st and last
                if xmlcell.text.find("=") <> -1:
                    k,v = xmlcell.text.split("=")
                    if k == field:
                        _dm.append(v)
                else:
                    _dm.append(xmlcell.text)
            dm.append(_dm)
        return dm
    
    def tearDown(self):
        shutil.copyfile(self.dbname+".backup",self.dbname)
        
        
class Test_Pivot_Student(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
        
        expected_results = ['Humanities','Math']
            
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                               yaxis="dow",ztypes="subject",source_type="student",
                               source_value="Clayton")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        
        self.assertListEqual(results,expected_results)

    def test_filter(self):

        expected_results = ['Math']
            
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                               yaxis="dow",ztypes="subject",source_type="student",
                               source_value="Clayton",cnstr_dow="WE")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
        
    def test_adult_xaxis(self):
        # this is the xml to define a 1 by 2 grid - Amelia/?? - 830/910 and then Math,??,Student News and Humanities
        expected_results = '<root><parser><value>drawnoformatgrid</value></parser><row><cell><bgcolor>#ffffff</bgcolor><valuetype>adult</valuetype><fgcolor>#000000</fgcolor><value /></cell><cell><bgcolor>#ffffff</bgcolor><valuetype>adult</valuetype><fgcolor>#000000</fgcolor><value>Amelia</value></cell><cell><bgcolor>#ffffff</bgcolor><valuetype>adult</valuetype><fgcolor>#000000</fgcolor><value>Stan</value></cell></row><row><cell><bgcolor>#ffffff</bgcolor><valuetype>period</valuetype><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell><subrow><subcell><valuetype>subject</valuetype><value>Humanities</value></subcell></subrow></cell><cell /></row><row><cell><bgcolor>#ffffff</bgcolor><valuetype>period</valuetype><fgcolor>#000000</fgcolor><value>910-950</value></cell><cell /><cell><subrow><subcell><valuetype>subject</valuetype><value>Math</value></subcell></subrow></cell></row></root>'
        
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                               yaxis="adult",ztypes="subject",source_type="student",
                               source_value="Clayton")    

        self.assertEqual(buf,expected_results)
        
    def tearDown(self):
        Test_Base.tearDown(self)
        
class Test_Pivot_Adult(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
        
        expected_results = ['Humanities']
            
        buf = ssrest.restquery(self.url + "adult/Amelia",xaxis="period",
                               yaxis="dow",ztypes="subject",source_type="adult",
                               source_value="Amelia")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        
        self.assertListEqual(results,expected_results)
        
class Test_Pivot_Subject(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
        
        expected_results = ['Amelia']
            
        buf = ssrest.restquery(self.url + "subject/Humanities",xaxis="period",
                               yaxis="dow",ztypes="adult",source_type="subject",
                               source_value="Humanities")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        
        self.assertListEqual(results,expected_results)
        
    def test_subject_student_axes(self):
        
        expected_results = ['Amelia']
            
        buf = ssrest.restquery(self.url + "subject/Humanities",xaxis="subject",
                               yaxis="student",ztypes="adult",source_type="subject",
                               source_value="Humanities")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        
        self.assertListEqual(results,expected_results)
        
class Test_Update_UID(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):

        expected_results = ['Student News']
                
        ssrest.restquery(self.url + "update/046CE5DA",
                         value_changes="subject,Student News") 

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="MO")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
        
class Test_Update(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_update_subject(self):

        expected_results = ['Humanities']
                
        ssrest.restquery(self.url + "update/02B1EEDC",
                         value_changes="subject,Humanities") 

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="WE")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
        
    def test_update_subject_object(self):
        ssrest.restquery(self.url + "update/054C4D26",
                         value_changes="subject,Math")
        
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='id,subject,dm',
                                   objref=0,
                                   pprint=1,
                                   constraints="dow='TU'",)

        objvals = self._parsedmdump(results,'id')
        
        # check id and dmid are equals
        self.assertEquals(objvals[0][0],objvals[0][-1])
        
        # check id <> orig id
        self.assertNotEquals(objvals[0][0],"054C4D26")
        
        # check dmid <> orig id
        self.assertNotEquals(objvals[0][-1],"054C4D26")
        
        # check subject has been updated
        self.assertEquals(objvals[0][1],"Math")
        
    def test_2_subject_updates(self):
        
        sleep(1)
        
        # server already has state post execution of test_
        expected_results = 'Humanities' 

        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='id,subject,dm',
                                   objref=0,
                                   pprint=1,
                                   constraints="dow='TU'",)

        newid = self._parsedmdump(results,'id')[0][0]
        
        ssrest.restquery(self.url + "update/"+newid,
                         value_changes="subject,Humanities")    

        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='id,subject,dm',
                                   objref=0,
                                   pprint=1,
                                   constraints="dow='TU'",)

        self.assertEquals(self._parsedmdump(results,'id')[0][1],expected_results)
        
    ''''def test_multi_subject_updates_direct(self):
        
        # ie using the new id provided by the rest call

        expected_results = ['Math']
        
        newid = ssrest.restquery(self.url + "update/054C4D26",
                         value_changes="subject,Humanities")
        newid = ssrest.restquery(self.url + "update/"+newid,
                         value_changes="subject,Math") 
        
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="TU")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)'''

        
    def test_update_adult(self):

        expected_results = ['Stan']
        
        ssrest.restquery(self.url + "update/054C4D26",
                         value_changes="teacher,Stan") 

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="adult",source_type="student",
                           source_value="Clayton",cnstr_dow="TU")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
        
        

    def tearDown(self):

        Test_Base.tearDown(self)


class Test_Add_Lesson(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):

        expected_results =[[u'Clayton', u'??', u'Math', u'830-910', u'MO'], 
                           [u'Clayton', u'??', u'??', u'830-910', u'WE'], 
                           [u'Clayton', u'??', u'Student News', u'830-910', u'TH'], 
                           [u'Clayton', u'Amelia', u'Humanities', u'830-910', u'TU'], 
                           [u'Clayton', u'??', u'Humanities', u'830-910', u'FR'], 
                           [u'Clayton', u'Stan', u'Math', u'830-910', u'TU']]
        
        expected_results = [[u'Clayton', u'Amelia', u'Humanities', u'830-910', u'TU'], 
                            [u'Clayton', u'Stan', u'Math', u'910-950', u'WE'], 
                            [u'Clayton', u'Stan', u'Math', u'830-910', u'TU']]
                
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='830-910',
                         recordtype='subject',dow='TU')
        
        db = Database(self.dbname)
        
        with db:
            _,rows,_ = tbl_rows_get(db,'lesson',['student','teacher','subject','period','dow'])
       
        self.assertListEqual(expected_results,rows)
        
    def test_object(self):

        expected_results ='<table><tr><td>ROOT</td><td>Clayton</td><td>Amelia</td><td>Humanities</td><td>TU</td><td>830-910</td><td>lesson</td></tr><tr><td>ROOT</td><td>Clayton</td><td>Stan</td><td>Math</td><td>WE</td><td>910-950</td><td>lesson</td></tr><tr><td>ROOT</td><td>Clayton</td><td>Stan</td><td>Math</td><td>None</td><td>830-910</td><td>lesson</td></tr></table>'
        
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='830-910',
                         recordtype='subject',dow='Tuesday')
        
        results = ssrest.restquery(self.url + "command/dump",
                         objtypes='lesson',
                         fields='student,adult,subject,dow,period',
                         pprint=1)
        
        self.assertEqual(expected_results,results)
        
    def tearDown(self):
        Test_Base.tearDown(self)
        
class Test_Add_Ref(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_period_object(self):

        # this does not give everything because we have not 
        # loaded the ref data 
        # ssrest.restquery(self.url + "load/period")
        expected_results = '<table><tr><td>ROOT</td><td>830-910</td><td>period</td></tr><tr><td>ROOT</td><td>910-950</td><td>period</td></tr><tr><td>ROOT</td><td>330-410</td><td>period</td></tr></table>'
        ssrest.restquery(self.url + "add/period",
                         name='330-410',code='330')
        
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='period',
                                   fields='name',
                                   pprint=1)
        
        self.assertEqual(expected_results,results)

    def test_period_db(self):

        expected_results = [[u'830-910', u'830', u'1'], 
                            [u'910-950', u'910', u'2'], 
                            [u'330-410', u'330', u'3']]
        
        ssrest.restquery(self.url + "add/period",
                         name='330-410',code='330')

        db = Database(self.dbname)
        
        with db:
            _,rows,_ = tbl_rows_get(db,'period',['name','code','enum'])
            
        self.assertListEqual(expected_results,rows)
        
        
    def tearDown(self):
        Test_Base.tearDown(self)

class Test_Add_Lesson_With_New_Ref(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_period_object(self):

        expected_results = '<table><tr><td>ROOT</td><td>430-510</td><td>lesson</td></tr></table>';
        
        ssrest.restquery(self.url + "add/period",
                         name='430-510',code='330')
                
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='430-510',
                         recordtype='subject',dow='TU')
        
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='period',
                                   constraints="period='430-510'",
                                   pprint=1)

        self.assertEqual(expected_results,results)
        
class Test_Add_Lesson_Update_to_New_Ref(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_period_object(self):

        expected_results = '<table><tr><td>ROOT</td><td>430-510</td><td>lesson</td></tr></table>';
        
        buf = ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='910-950',
                         recordtype='subject',dow='TU')

        ssrest.restquery(self.url + "add/period",
                         name='430-510',code='430')
        
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='id,subject,dm',
                                   objref=0,
                                   pprint=1,
                                   constraints="dow='TU',period='910-950'",)

        objvals = self._parsedmdump(results,'id')
                
        ssrest.restquery(self.url + "update/"+objvals[0][0],
                         value_changes="period,430-510")         
                
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='period',
                                   constraints="period='430-510'",
                                   pprint=1)

        self.assertEqual(expected_results,results)
        
class Test_SearchByID(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):
        
        expected_result = '<root><parser><value>drawform</value></parser><item id="1"><value>wp</value><valuetype>recordtype</valuetype></item><item id="2"><value>830-910</value><valuetype>period</valuetype></item><item id="3"><value>Amelia</value><valuetype>adult</valuetype></item><item id="4"><value>Clayton</value><valuetype>student</valuetype></item><item id="5"><value>TU</value><valuetype>dow</valuetype></item><item id="6"><value>Humanities</value><valuetype>subject</valuetype></item></root>'
        
        result = ssrest.restquery(self.url + "id/054C4D26")
        self.assertEqual(expected_result,result)
        
    def tearDown(self):
        Test_Base.tearDown(self)
          
class Test_New(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):
        
        expected_result = '<root><parser><value>drawform</value></parser><item id="1"><value /><valuetype>recordtype</valuetype></item><item id="2"><value /><valuetype>period</valuetype></item><item id="3"><value /><valuetype>adult</valuetype></item><item id="4"><value /><valuetype>student</valuetype></item><item id="5"><value /><valuetype>dow</valuetype></item><item id="6"><value /><valuetype>subject</valuetype></item></root>'
        
        result = ssrest.restquery(self.url + "new/lesson")
        self.assertEqual(expected_result,result)
        
    def tearDown(self):
        Test_Base.tearDown(self)
          
class Test_Dump(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
        
        expected_results = '<table><tr><td>ROOT</td><td>830-910</td><td>Humanities</td><td>lesson</td></tr><tr><td>ROOT</td><td>910-950</td><td>Math</td><td>lesson</td></tr></table>'
        
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='period,subject',
                                   objref=0,
                                   pprint=1)
        
        self.assertEqual(expected_results,results)
        
    def tearDown(self):
        Test_Base.tearDown(self)
        
class Test_LoadRef(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
    
        ssrest.restquery(self.url + "load/period")
        
        numperiods = ssrest.restquery(self.url + "command/dump",
                                              objtypes='period',
                                              fields='name',
                                              count=0)
        
        self.assertEqual(numperiods,'2')
        
    def test_subject(self):
    
        ssrest.restquery(self.url + "load/subject")
        
        numperiods = ssrest.restquery(self.url + "command/dump",
                                              objtypes='subject',
                                              fields='name',
                                              count=0)
        
        self.assertEqual(numperiods,'4')
        
class Test_Reload(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
        
        # test reload works by adding a row and checking the count after reload
        # is one more than before
        expected_results = ['Humanities','Math','Humanities','??','Student News']
           
    
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='830-910',
                         recordtype='subject',dow='TU') 

        pre_count = ssrest.restquery(self.url + "command/dump",
                                              objtypes='lesson',
                                              #fields='student,adult,subject,dow,period,id',
                                              fields='id,__timestamp',
                                              count=0)

        
        results = ssrest.restquery(self.url + "command/reload",unknown="Y")
                
        post_count = ssrest.restquery(self.url + "command/dump",
                                              objtypes='lesson',
                                              #fields='student,adult,subject,dow,period,id',
                                              fields='id,__timestamp',
                                              count=0)

        self.assertEquals(pre_count,'3')
        self.assertEquals(post_count,'2')
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Update))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SearchByID))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_New))    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Lesson))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_LoadRef))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Ref))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Lesson_With_New_Ref))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Lesson_Update_to_New_Ref))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Reload))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Dump))
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Update_UID))'''
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Adult))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Subject))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 