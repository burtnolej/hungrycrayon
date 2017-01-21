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
    
    def tearDown(self):
        shutil.copyfile(self.dbname+".backup",self.dbname)
        
        
class Test_Pivot_Student(Test_Base):
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
        
    def test_adult_xaxis(self):
        # this is the xml to define a 1 by 2 grid - Amelia/?? - 830/910 and then Math,??,Student News and Humanities
        expected_results = '<root><parser><value>drawnoformatgrid</value></parser><row><cell><bgcolor>#ffffff</bgcolor><valuetype>adult</valuetype><fgcolor>#000000</fgcolor><value /></cell><cell><bgcolor>#ffffff</bgcolor><valuetype>adult</valuetype><fgcolor>#000000</fgcolor><value>??</value></cell><cell><bgcolor>#ffffff</bgcolor><valuetype>adult</valuetype><fgcolor>#000000</fgcolor><value>Amelia</value></cell></row><row><cell><bgcolor>#ffffff</bgcolor><valuetype>period</valuetype><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell><subrow><subcell><valuetype>subject</valuetype><value>Math</value></subcell></subrow><subrow><subcell><valuetype>subject</valuetype><value>??</value></subcell></subrow><subrow><subcell><valuetype>subject</valuetype><value>Student News</value></subcell></subrow><subrow><subcell><valuetype>subject</valuetype><value>Humanities</value></subcell></subrow></cell><cell><subrow><subcell><valuetype>subject</valuetype><value>Humanities</value></subcell></subrow></cell></row></root>'
        
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
        
        expected_results = ['Clayton','Clayton']
            
        buf = ssrest.restquery(self.url + "subject/Humanities",xaxis="period",
                               yaxis="dow",ztypes="student",source_type="subject",
                               source_value="Humanities")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        
        self.assertListEqual(results,expected_results)
        
    '''def test_subject_student_axes(self):
        
        expected_results = ['Clayton','Clayton']
            
        buf = ssrest.restquery(self.url + "subject/Humanities",xaxis="subject",
                               yaxis="student",ztypes="student",source_type="subject",
                               source_value="Humanities")    

        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        
        self.assertListEqual(results,expected_results)'''
        
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

        expected_results = ['Student News']
                
        ssrest.restquery(self.url + "update/046CE5DA",
                         value_changes="subject,Student News") 

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="MO")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
        
    def test_2_subject_updates(self):
        
        sleep(1)
        
        # server already has state post execution of test_
        expected_results = ['Math']  

        ssrest.restquery(self.url + "update/054C4D26",
                         value_changes="subject,Math")    


        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="TU")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)
                
    def test_multi_subject_updates(self):

        expected_results = ['Math']
        
        newid = ssrest.restquery(self.url + "update/05C8F56C",
                         value_changes="subject,Humanities")
        newid = ssrest.restquery(self.url + "update/"+newid,
                         value_changes="subject,Student News") 
        newid = ssrest.restquery(self.url + "update/"+newid,
                         value_changes="subject,Humanities")
        newid = ssrest.restquery(self.url + "update/"+newid,
                         value_changes="subject,Math") 

        
        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="subject",source_type="student",
                           source_value="Clayton",cnstr_dow="TH")    
    
        results = self._getelementstext(self._queryxml(buf,".//subcell[valuetype]","value"))
        self.assertListEqual(results,expected_results)

        
    def test_update_adult(self):

        expected_results = ['Stan']
                
        ssrest.restquery(self.url + "add/adult",
                         name='Stan',code='STAN')
        
        ssrest.restquery(self.url + "update/046CE5DA",
                         value_changes="teacher,Stan") 

        buf = ssrest.restquery(self.url + "student/Clayton",xaxis="period",
                           yaxis="dow",ztypes="adult",source_type="student",
                           source_value="Clayton",cnstr_dow="MO")    
    
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
                
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='830-910',
                         recordtype='subject',dow='Tuesday')
        
        db = Database(self.dbname)
        
        with db:
            _,rows,_ = tbl_rows_get(db,'lesson',['student','teacher','subject','period','dow'])
       
        self.assertListEqual(expected_results,rows)
        
    def test_object(self):

        expected_results ='<table><tr><td>ROOT</td><td>Clayton</td><td>??</td><td>Math</td><td>MO</td><td>830-910</td><td>lesson</td></tr><tr><td>ROOT</td><td>Clayton</td><td>??</td><td>??</td><td>WE</td><td>830-910</td><td>lesson</td></tr><tr><td>ROOT</td><td>Clayton</td><td>??</td><td>Student News</td><td>TH</td><td>830-910</td><td>lesson</td></tr><tr><td>ROOT</td><td>Clayton</td><td>Amelia</td><td>Humanities</td><td>TU</td><td>830-910</td><td>lesson</td></tr><tr><td>ROOT</td><td>Clayton</td><td>??</td><td>Humanities</td><td>FR</td><td>830-910</td><td>lesson</td></tr><tr><td>ROOT</td><td>Clayton</td><td>Stan</td><td>Math</td><td>TU</td><td>830-910</td><td>lesson</td></tr></table>'
        
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
        expected_results = '<table><tr><td>ROOT</td><td>830-910</td><td>period</td></tr><tr><td>ROOT</td><td>330-410</td><td>period</td></tr></table>';        

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
                            [u'950-1030', u'950', u'3'], 
                            [u'1030-1110', u'1030', u'4'], 
                            [u'1110-1210', u'1110', u'5'], 
                            [u'1210-100', u'1210', u'6'], 
                            [u'100-140', u'1310', u'7'], 
                            [u'140-220', u'1340', u'8'],
                            [u'220-300', u'1420', u'9'], 
                            [u'300-330', u'1500', u'10'], 
                            [u'330-410', u'330', u'11']]
        
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

        expected_results = '<table><tr><td>ROOT</td><td>330-410</td><td>lesson</td></tr></table>';
        
        ssrest.restquery(self.url + "add/period",
                         name='330-410',code='330')
                
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='330-410',
                         recordtype='subject',dow='Tuesday')
        
        ssrest.restquery(self.url + "update/046CE5DA",
                         value_changes="subject,Student News") 
        
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='period',
                                   constraints="period='330-410'",
                                   pprint=1)

        self.assertEqual(expected_results,results)
        
class Test_Add_Lesson_Update_to_New_Ref(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_period_object(self):

        expected_results = '<table><tr><td>ROOT</td><td>330-410</td><td>lesson</td></tr></table>';
        
        buf = ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='300-330',
                         recordtype='subject',dow='Tuesday')

        #ssrest.restquery(self.url + "add/period",
        #                 name='330-410',code='330')
        
        print self._getelementstext(self._queryxml(buf,".//item[2]","value"))[0]
        
        #ssrest.restquery(self.url + "update/046CE5DA",
        #                 value_changes="subject,Student News")         
                
        '''results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson',
                                   fields='period',
                                   constraints="period='330-410'",
                                   pprint=1)

        self.assertEqual(expected_results,results)'''
        
class Test_SearchByID(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
        
    def test_(self):
        
        expected_result = '<root><parser><value>drawform</value></parser><item id="1"><value>wp</value><valuetype>recordtype</valuetype></item><item id="2"><value>830-910</value><valuetype>period</valuetype></item><item id="3"><value>??</value><valuetype>adult</valuetype></item><item id="4"><value>Clayton</value><valuetype>student</valuetype></item><item id="5"><value>MO</value><valuetype>dow</valuetype></item><item id="6"><value>Math</value><valuetype>subject</valuetype></item></root>'
        
        result = ssrest.restquery(self.url + "id/046CE5DA")
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
        
        expected_results = '<table><tr><td>1.1.2.8.4</td><td>-</td><td>-</td><td>830-910</td><td>period</td></tr><tr><td>ROOT</td><td>830-910</td><td>Math</td><td>-</td><td>lesson</td></tr><tr><td>1.4.2.8.17</td><td>-</td><td>-</td><td>830-910</td><td>period</td></tr><tr><td>ROOT</td><td>830-910</td><td>??</td><td>-</td><td>lesson</td></tr><tr><td>1.3.2.8.5</td><td>-</td><td>-</td><td>830-910</td><td>period</td></tr><tr><td>ROOT</td><td>830-910</td><td>Student News</td><td>-</td><td>lesson</td></tr><tr><td>1.2.2.6.22</td><td>-</td><td>-</td><td>830-910</td><td>period</td></tr><tr><td>ROOT</td><td>830-910</td><td>Humanities</td><td>-</td><td>lesson</td></tr><tr><td>1.5.2.8.22</td><td>-</td><td>-</td><td>830-910</td><td>period</td></tr><tr><td>ROOT</td><td>830-910</td><td>Humanities</td><td>-</td><td>lesson</td></tr><tr><td>ROOT</td><td>-</td><td>-</td><td>830-910</td><td>period</td></tr></table>'
            
        results = ssrest.restquery(self.url + "command/dump",
                                   objtypes='lesson,period',
                                   fields='period,subject,name',
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
        
        self.assertEqual(numperiods,'10')
        
class Test_Reload(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,"test_ssviewer_rest.sqlite",8080)
 
    def test_(self):
        
        # test reload works by adding a row and checking the count after reload
        # is one more than before
        expected_results = ['Humanities','Math','Humanities','??','Student News']
           
    
        ssrest.restquery(self.url + "add/lesson",
                         student='Clayton',teacher='Stan',subject='Math',period='830-910',
                         recordtype='subject',dow='Tuesday') 

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

        self.assertEquals(pre_count,'6')
        self.assertEquals(post_count,'5')
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Update))
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SearchByID))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_New))    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Lesson))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_LoadRef))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Reload))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Dump))'''
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Ref))
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Lesson_With_New_Ref))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Lesson_Update_to_New_Ref))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Update_UID))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Adult))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Subject))'''
    
    unittest.TextTestRunner(verbosity=2).run(suite) 