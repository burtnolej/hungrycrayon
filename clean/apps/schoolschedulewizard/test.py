import unittest

from misc_utils_selenium import *
'''from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
'''

# java -jar selenium-server-standalone-2.53.0.jar -Dwebdriver.gecko.driver=/usr/local/bin/geckodriver

import os
import time

#baseurl = "http://www.hungrycrayon.com"
#baseurl = "http://192.168.1.254"
baseurl = "http://0.0.0.0"
page="dpivot.php"


'''
fucia.sqlite -> ../apps/schoolschedulewizard/test_ssviewer_rest.sqlite
python ./ssviewer_rest.py --allow-unknown
java -jar selenium-server-standalone-2.53.0.jar -Dwebdriver.gecko.driver=/usr/local/bin/geckodriver

run selenium-reset.sh 

'''
       
    
class Test_Base(unittest.TestCase):
    
    def setUp(self):
    
        self.browser = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)    

        _url = [baseurl,page]
        self.url = "/".join(_url)
        self.browser.get(self.url)
      
class Test_Pivot_Add_Datafields(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
    
    
    
class Test_Pivot_Student(Test_Base):

    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        time.sleep(1)

        expected_results = [u'Humanities', u'Math']
        
        set_select_element("source_value","Clayton",self.browser)
        set_checkbox_element("subject",self.browser)

        time.sleep(1)
        results = get_table_values(self.browser)
        
        self.assertListEqual(results,expected_results)
        
        
    def test_filter(self):
        
        time.sleep(1)
        expected_results = [u'Humanities']
        set_select_element("source_value","Clayton",self.browser)
        set_checkbox_element("subject",self.browser)
        set_select_element("cnstr_dow","TU",self.browser)

        time.sleep(1)
        results = get_table_values(self.browser)
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Pivot_Adult(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        expected_results = [u'Humanities']
        set_select_element("source_type","adult",self.browser)
        time.sleep(1)
        set_select_element("source_value","Amelia",self.browser)
        set_checkbox_element("subject",self.browser)

        time.sleep(1)
        results = get_table_values(self.browser)
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        self.browser.quit()
     
class Test_Add_Ref(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_adult(self):
        expected_results = [u'code', u'name', u'enum', u'objtype', u'userobjid', 
                            u'Amelia', u'Amelia', u'0', u'adult', u'Amelia', 
                            u'Stan', u'Stan', u'2', u'adult', u'Stan', 
                            u'Brian', u'Brian', u'3', u'adult', u'Brian']

        _macro_add_new_record(self.browser,"adult",dict(name="Brian",code="Brian"))
        _macro_list_objects(self.browser,"adult")
        results = get_table_values(self.browser,suppressid=True)

        self.assertListEqual(results,expected_results)
        
        # check that item has been added to other dropdowns
        
        # new page
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'lesson',self.browser)
        select_elements = get_elements(self.browser,'select','name')
        adult_expected_results = [u'NotSelected', u'All', u'Amelia', u'Stan',u'Brian']
        
        #print adult_expected_results,select_elements['teacher']
        
        self.assertEqual(adult_expected_results,select_elements['teacher'])
        
        # pivot page
        click_menu_element("dpivot.php",self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'select','name')
        adult_expected_results = [u'NotSelected', u'All', u'Amelia', u'Stan',u'Brian']
        
        #print adult_expected_results,select_elements['cnstr_adult']
        self.assertEqual(adult_expected_results,select_elements['cnstr_adult'])
        
    def test_period(self):

        expected_results = [u'code', u'name', u'enum', u'objtype', u'userobjid', 
                            u'830-910', u'830-910', u'0', u'period', u'830-910', 
                            u'910-950', u'910-950', u'2', u'period', u'910-950', 
                            u'400', u'400-430', u'3', u'period', u'400-430']
        
        _macro_add_new_record(self.browser,"period",dict(name="400-430",code="400"))
        _macro_list_objects(self.browser,"period")
        results = get_table_values(self.browser,suppressid=True)
        self.assertListEqual(results,expected_results)
        
        # check that item has been added to other dropdowns
        
        # new page
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'lesson',self.browser)
        select_elements = get_elements(self.browser,'select','name')
        period_expected_results = [u'NotSelected', u'All', u'830-910', u'910-950',u'400-430']
        self.assertEqual(period_expected_results,select_elements['period'])
        
        # pivot page
        click_menu_element("dpivot.php",self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'select','name')
        period_expected_results = [u'NotSelected', u'All', u'830-910', u'910-950',u'400-430']
        self.assertEqual(period_expected_results,select_elements['cnstr_period'])
        
    def test_student(self):
        
        expected_results = [u'code', u'name', u'enum', u'objtype', u'userobjid', 
                            u'Clayton', u'Clayton', u'0', u'student', u'Clayton', 
                            u'JB', u'Jon', u'2', u'student', u'Jon']
        
        _macro_add_new_record(self.browser,"student",dict(name="Jon",code="JB",prep="5"))
        _macro_list_objects(self.browser,"student")
        results = get_table_values(self.browser,suppressid=True)
        self.assertListEqual(results,expected_results)
        
        # new page
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'lesson',self.browser)
        select_elements = get_elements(self.browser,'select','name')
        student_expected_results = [u'NotSelected', u'All', u'Clayton', u'Jon']
        self.assertEqual(student_expected_results,select_elements['student'])
        
        # pivot page
        click_menu_element("dpivot.php",self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'select','name')
        student_expected_results = [u'NotSelected', u'All', u'Clayton', u'Jon']
        self.assertEqual(student_expected_results,select_elements['cnstr_student'])
    
    def test_dow(self):
       
        expected_results = [u'code', u'name', u'enum', u'objtype', u'userobjid', 
                            u'TU', u'TU', u'0', u'dow', u'TU', 
                            u'WE', u'WE', u'2', u'dow', u'WE',
                            u'FU', u'FU', u'3', u'dow', u'FU']
        
        _macro_add_new_record(self.browser,"dow",dict(name="FU",code="FU"))
        _macro_list_objects(self.browser,"dow")
        results = get_table_values(self.browser,suppressid=True)
        self.assertListEqual(results,expected_results)
        
        # new page
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'lesson',self.browser)
        select_elements = get_elements(self.browser,'select','name')
        dow_expected_results = [u'NotSelected', u'All', u'TU', u'WE',u'FU']
        self.assertEqual(dow_expected_results,select_elements['dow'])
        
        # pivot page
        click_menu_element("dpivot.php",self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'select','name')
        dow_expected_results = [u'NotSelected', u'All', u'TU', u'WE',u'FU']
        self.assertEqual(dow_expected_results,select_elements['cnstr_dow'])
        
    def test_subject(self):
        expected_results = [u'code', u'name', u'enum', u'objtype', u'userobjid', 
                            u'Humanities', u'Humanities', u'0', u'subject', u'Humanities', 
                            u'Math', u'Math', u'2', u'subject', u'Math', 
                            u'CYCL', u'cycling', u'3', u'subject', u'cycling']

        _macro_add_new_record(self.browser,"subject",dict(name="cycling",code="CYCL"))

        _macro_list_objects(self.browser,"subject")
        
        results = get_table_values(self.browser,suppressid=True)
        
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        self.browser.quit()

class Test_Select_Options(Test_Base):
    
    # note that the results include everything thats been changed in the earlier tests
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_pivot(self):

        
        results = get_table_values(self.browser,True)

        #self.assertListEqual(results,expected_results)
        
        print results
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Add_Lesson(Test_Base):
    
    # note that the results include everything thats been changed in the earlier tests
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        expected_results = [u'status', u'substatus', u'recordtype', u'period', u'dow', u'source', u'session', u'adult', u'student', u'objtype', u'prep', u'userobjid', u'subject', 
                            u'master', u'complete', u'wp', u'830-910', u'TU', u'dbinsert', u'Amelia.Humanities.Tuesday.830-910', u'Amelia', u'Clayton', u'lesson', u'5', u'1.2.2.6.22', u'Humanities', 
                            u'master', u'complete', u'academic', u'910-950', u'WE', u'dbinsert', u'Stan.Math.Wednesday.910-950', u'Stan', u'Clayton', u'lesson', u'5', u'1.2.3.4.5', u'Math', 
                            u'master', u'complete', u'subject', u'400-430', u'FU', u'manual', u'Stan.cycling.FU.400-430', u'Stan', u'Jon', u'lesson', u'5', u'3.3.2.None.3', u'cycling']
        
                
        _macro_add_new_record(self.browser,"lesson",dict(recordtype="seminar",period="400-430",
                                                         teacher="Stan", student="Jon",
                                                         dow="FU",subject="cycling"))

        _macro_list_objects(self.browser,"lesson")
        
        results = get_table_values(self.browser,suppressid=True)

        self.assertListEqual(results,expected_results)

        
    def tearDown(self):
        self.browser.quit()

    
class Test_Search_By_Criteria(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        

        expected_results =   [u'code', u'name', u'enum', u'objtype', u'userobjid', 
                              u'830-910', u'830-910', u'0', u'period', u'830-910', 
                              u'910-950', u'910-950', u'2', u'period', u'910-950']
               
        _macro_list_objects(self.browser,"period")
        
        results = get_table_values(self.browser,suppressid=True)
        
        self.assertListEqual(results,expected_results)
        
    def test_filter(self):

        expected_results = [u'status', u'substatus', u'recordtype', u'period', u'dow', u'source', u'session', u'adult', u'student', u'objtype', u'prep', u'userobjid', u'subject', 
                            u'master', u'complete', u'wp', u'830-910', u'TU', u'dbinsert', u'Amelia.Humanities.Tuesday.830-910', u'Amelia', u'Clayton', u'lesson', u'5', u'1.2.2.6.22', u'Humanities']
        
        _macro_list_objects(self.browser,"lesson",dict(subject='Humanities'))
        
        results = get_table_values(self.browser,suppressid=True)
        
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        self.browser.quit()
        pass
       
class Test_Pivot_Select(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        self.select_elements = get_elements(self.browser,'select','name')

    def test_main(self):
        # test_yaxis(self):
        expect_results_yaxis = [u'Period', u'Dow', u'Adult', u'Subject', u'Student']
        
        self.assertListEqual(self.select_elements['yaxis'],expect_results_yaxis)
        
        # test_xaxis(self):    
        expect_results_xaxis = [u'Period', u'Dow', u'Adult', u'Subject', u'Student']
        self.assertListEqual(self.select_elements['xaxis'],expect_results_xaxis)
            
        # test_filter_adult(self):
        expect_results_cnstr_adult = [u'NotSelected', u'All', u'Amelia', u'Stan']
        self.assertListEqual(self.select_elements['cnstr_adult'],expect_results_cnstr_adult)
        
        # test_filter_recordtype(self):
        expect_results_cnstr_recordtype = [u'NotSelected', u'All', u'Wp', u'Ap', u'Academic', u'Seminar']
        self.assertListEqual(self.select_elements['cnstr_recordtype'],expect_results_cnstr_recordtype)
         
        # test_filter_student(self):
        expect_results_cnstr_student = [u'NotSelected', u'All', u'Clayton']
        self.assertListEqual(self.select_elements['cnstr_student'],expect_results_cnstr_student)
         
        # test_filter_source(self):
        expect_results_cnstr_source = [u'NotSelected', u'All', u'Dbinsert']
        self.assertListEqual(self.select_elements['cnstr_source'],expect_results_cnstr_source)
         
        # test_filter_subject(self):
        expect_results_cnstr_subject = [u'NotSelected', u'All', u'Humanities', u'Math']
        self.assertListEqual(self.select_elements['cnstr_subject'],expect_results_cnstr_subject)

        # test_filter_dow(self):
        expect_results_cnstr_dow = [u'NotSelected', u'All', u'TU', u'WE']
        self.assertListEqual(self.select_elements['cnstr_dow'],expect_results_cnstr_dow)
         
        # test_filter_prep(self):
        expect_results_cnstr_prep = [u'NotSelected', u'All', u'5']
        self.assertListEqual(self.select_elements['cnstr_prep'],expect_results_cnstr_prep)
     
        # test_period(self):
        expect_results_cnstr_period = [u'NotSelected', u'All', u'830-910', u'910-950']  
        self.assertListEqual(self.select_elements['cnstr_period'],expect_results_cnstr_period)

        # source_type = "Student"
        # test_source_type(self):
        expect_results_source_type = [u'Student', u'Adult', u'Subject']
        self.assertListEqual(self.select_elements['source_type'],expect_results_source_type)

        # test_source_value(self):
        expect_results_source_value = [u'NotSelected', u'All', u'Clayton']
        self.assertListEqual(self.select_elements['source_value'],expect_results_source_value)
        
    def test_main_adult(self):
        
        # source_type = "Student"
        set_select_element("source_type",'adult',self.browser)
        self.select_elements = get_elements(self.browser,'select','name')
        
        time.sleep(3)
        expected_results = [u'NotSelected', u'All', u'Amelia', u'Stan']
        
        self.assertListEqual(self.select_elements['source_value'],expected_results)
        
    def test_main_subject(self):
        
        # source_type = "Student"
        set_select_element("source_type",'subject',self.browser)
        self.select_elements = get_elements(self.browser,'select','name')
        
        expected_results = [u'NotSelected', u'All', u'Humanities', u'Math']

        self.assertListEqual(self.select_elements['source_value'],expected_results)
        
class Test_New_Select(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_lesson(self):
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'lesson',self.browser)
        select_elements = get_elements(self.browser,'select','name')
        
        expected_results = [u'dow', u'period', u'recordtype', u'source_value', u'student', u'subject', u'teacher']
        
        # source_value
        source_value_expected_results = [u'Not Selected', u'Lesson', u'Subject', u'Student', u'Adult', u'Period', u'Dow', u'Recordtype']
        
        # source value = 'lesson'
        recordtype_expected_results = [u'NotSelected', u'All', u'Subject', u'Wp', u'Ap']
        period_expected_results = [u'NotSelected', u'All', u'830-910', u'910-950']
        dow_expected_results = [u'NotSelected', u'All',u'TU', u'WE'] 
        student_expected_results = [u'NotSelected', u'All', u'Clayton']         
        teacher_expected_results = [u'NotSelected', u'All', u'Amelia','Stan']
        subject_expected_results = [u'NotSelected', u'All', u'Humanities','Math']      

        self.assertEqual(recordtype_expected_results,select_elements['recordtype'])
        self.assertEqual(period_expected_results,select_elements['period'])
        self.assertEqual(dow_expected_results,select_elements['dow'])
        self.assertEqual(student_expected_results,select_elements['student'])
        self.assertEqual(teacher_expected_results,select_elements['teacher'])
        self.assertEqual(subject_expected_results,select_elements['subject'])
        
        element_names = select_elements.keys()
        element_names.sort()
        
        self.assertEqual(element_names,expected_results)
  
    def test_period(self):
        
        code_expected_results = [u'']
        name_expected_results = [u'']
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'period',self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'input','id',inputtype='text')
        
        self.assertEqual(code_expected_results,select_elements['code'])
        self.assertEqual(name_expected_results,select_elements['name'])
        
        self.assertEqual(select_elements.keys(),['code','name'])
        
        
    def test_subject(self):
        
        code_expected_results = [u'']
        name_expected_results = [u'']
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'subject',self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'input','id',inputtype='text')
        
        self.assertEqual(code_expected_results,select_elements['code'])
        self.assertEqual(name_expected_results,select_elements['name'])
        
        self.assertEqual(select_elements.keys(),['code','name'])
        
        
    def test_student(self):
        
        code_expected_results = [u'']
        name_expected_results = [u'']
        prep_expected_results = [u'']
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'student',self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'input','id',inputtype='text')
        
        self.assertEqual(code_expected_results,select_elements['code'])
        self.assertEqual(name_expected_results,select_elements['name'])
        self.assertEqual(prep_expected_results,select_elements['prep'])
        
        self.assertEqual(select_elements.keys(),['code','name','prep'])
        
    def test_dow(self):
        
        code_expected_results = [u'']
        name_expected_results = [u'']
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'dow',self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'input','id',inputtype='text')
        
        self.assertEqual(code_expected_results,select_elements['code'])
        self.assertEqual(name_expected_results,select_elements['name'])
        
        self.assertEqual(select_elements.keys(),['code','name'])
        
    def test_adult(self):
        
        code_expected_results = [u'']
        name_expected_results = [u'']
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'adult',self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'input','id',inputtype='text')
        
        self.assertEqual(code_expected_results,select_elements['code'])
        self.assertEqual(name_expected_results,select_elements['name'])
        
        self.assertEqual(select_elements.keys(),['code','name'])
        
    def test_dow(self):
        
        code_expected_results = [u'']
        name_expected_results = [u'']
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'dow',self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'input','id',inputtype='text')
        
        self.assertEqual(code_expected_results,select_elements['code'])
        self.assertEqual(name_expected_results,select_elements['name'])
        
        self.assertEqual(select_elements.keys(),['code','name'])
        
    def test_recordtype(self):
        
        code_expected_results = [u'']
        name_expected_results = [u'']
        
        click_menu_element("dnew.php",self.browser)
        time.sleep(0.5)
        set_select_element("source_value",'recordtype',self.browser)
        time.sleep(0.5)
        select_elements = get_elements(self.browser,'input','id',inputtype='text')
        
        self.assertEqual(code_expected_results,select_elements['code'])
        self.assertEqual(name_expected_results,select_elements['name'])
        
        self.assertEqual(select_elements.keys(),['code','name'])
        
    def tearDown(self):
        self.browser.quit()
        pass
        
'''class Test_Select_Options(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        click_menu_element("dnew.php",browser)
        time.sleep(0.5)
        set_select_element("source_value",'lesson',browser)
        
        print '''

class Test_Search_New(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        expected_results = [u'objtype', u'name', u'userobjid', u'period', u'830-910', u'830-910']
        
        _macro_list_objects(self.browser,"period")
        
        results = get_table_values(self.browser)
        
        self.assertListEqual(results,expected_results)
        
    def test_filter(self):
                
        expected_results = [u'status', u'substatus', u'recordtype', u'period', u'dow', u'source', u'session', u'adult', u'student', u'id', u'objtype', u'prep', u'userobjid', u'subject', 
                            u'master', u'complete', u'wp', u'830-910', u'TU', u'dbinsert', u'Amelia.Humanities.Tuesday.830-910', u'Amelia', u'Clayton', u'054C4D26', u'lesson', u'5', u'1.2.2.6.22', u'Humanities', 
                            u'master', u'incomplete', u'academic', u'830-910', u'FR', u'dbinsert', u'??.Humanities.Friday.830-910', u'??', u'Clayton', u'0434FD04', u'lesson', u'5', u'1.5.2.8.22', u'Humanities']
        
        _macro_list_objects(self.browser,"lesson",dict(subject='Humanities'))
        
        results = get_table_values(self.browser)
        
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        self.browser.quit()
        pass
    
class Test_Update(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        expected_results =  [u'status', u'substatus', u'recordtype', u'period', u'dow', u'source', u'session', u'adult', u'student', u'objtype', u'prep', u'userobjid', u'subject', 
                             u'master', u'complete', u'wp', u'400-430', u'TU', u'dbinsert', u'Amelia.Humanities.Tuesday.830-910', u'Amelia', u'Clayton', u'lesson', u'5', u'1.2.2.6.22', u'Humanities', 
                             u'master', u'complete', u'academic', u'910-950', u'WE', u'dbinsert', u'Stan.Math.Wednesday.910-950', u'Stan', u'Clayton', u'lesson', u'5', u'1.2.3.4.5', u'Math', 
                             u'master', u'complete', u'subject', u'400-430', u'FU', u'manual', u'Stan.cycling.FU.400-430', u'Stan', u'Jon', u'lesson', u'5', u'3.3.2.None.3', u'cycling']
        
        _macro_add_new_record(self.browser,"period",dict(name="400-430",code="400-430"))
        
        time.sleep(2)
        _macro_update_field(self.browser,"054C4D26",dict(period="400-430"))
        
        time.sleep(2)
        
        _macro_list_objects(self.browser,"lesson")
        
        time.sleep(2)
        results = get_table_values(self.browser,suppressid=True)
        
        self.assertListEqual(results,expected_results)
        
        # test that the update is reflected in the pivot
        
        expected_results = [u'', u'TU', u'WE', u'910-950', u'', u'Math', u'Math', u'400-430', u'Humanities', u'Humanities', u'']
        click_menu_element("dpivot.php",self.browser)
        set_select_element("source_value","Clayton",self.browser)
        set_checkbox_element("subject",self.browser)

        time.sleep(1)
        results = get_table_values(self.browser,xpathstr="//td")
        
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        self.browser.quit()
        pass

        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Search_By_Criteria))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Adult))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot_Select))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Ref))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Lesson))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Update))
    

    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 