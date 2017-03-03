import unittest
import ssviewer_rest_utils as ssrest
from misc_utils_selenium import *
import shutil

'''from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
'''

# java -jar selenium-server-standalone-2.53.0.jar -Dwebdriver.gecko.driver=/usr/local/bin/geckodriver

import os
import time

baseurl = "http://0.0.0.0"

class Test_Base(unittest.TestCase):
    
    def setUp(self,page):
    
        shutil.copyfile("test_webcore.sqlite.backup","test_webcore.sqlite")
        ssrest.restquery(baseurl + ":8080/command/reload",unknown="Y")
        
        self.browser = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)    

        _url = [baseurl,page]
        self.url = "/".join(_url)
        self.browser.get(self.url)
        
class Test_Popout_MultiSelect_DOW(Test_Base):

    def setUp(self):
        self.page = "popout_dow.php"
        Test_Base.setUp(self,self.page)
        
    def test_1select(self):
        
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=TU&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("TU",self.browser)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_2select(self):
        
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=TU,WE&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("TU",self.browser)
        time.sleep(0.1)
        set_checkbox_element("WE",self.browser)
        time.sleep(0.1)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_dimensions(self):
        
        click_popupmenu("handle1",self.browser)
        
        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")

        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,306)
        self.assertAlmostEqual(h,89)
        
    def test_sticky(self):

        click_popupmenu("handle1",self.browser)
    
        time.sleep(0.1)
        execute_script(self.browser, "window.location = 'http://0.0.0.0/"+self.page+"?'+ getAllInputValues('ztypes',['qunit-filter-input']);")
        time.sleep(0.1)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,306)
        self.assertAlmostEqual(h,89)
        
    def test_openclose(self):

        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.5)
        click_popupmenu("handle1",self.browser)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,-89)
        self.assertAlmostEqual(w,306)
        self.assertAlmostEqual(h,89)
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Popout_MultiSelect_DOW_Period(Test_Base):

    def setUp(self):
        self.page = "popout_dow_period.php"
        Test_Base.setUp(self,self.page)
        
    def test_1select(self):
                
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=TU&cnstr_period=830-910&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("830-910",self.browser)
        set_checkbox_element("TU",self.browser)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_2select(self):
        
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=TU,WE&cnstr_period=830-910,910-950&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("830-910",self.browser)        
        time.sleep(0.1)
        set_checkbox_element("TU",self.browser)
        time.sleep(0.1)
        set_checkbox_element("910-950",self.browser)     
        time.sleep(0.1)
        set_checkbox_element("WE",self.browser)
        time.sleep(0.1)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_dimensions(self):
        
        click_popupmenu("handle1",self.browser)
        
        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,306)
        self.assertAlmostEqual(h,159)

    def test_sticky(self):

        click_popupmenu("handle1",self.browser)
    
        time.sleep(0.1)
        execute_script(self.browser, "window.location = 'http://0.0.0.0/"+self.page+"?'+ getAllInputValues('ztypes',['qunit-filter-input']);")
        time.sleep(0.1)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,306)
        self.assertAlmostEqual(h,159)
        
    def test_openclose(self):

        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.5)
        click_popupmenu("handle1",self.browser)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,-160)
        self.assertAlmostEqual(w,306)
        self.assertAlmostEqual(h,159)
        
    def tearDown(self):
        self.browser.quit()
    
class Test_Popout_JSButton(Test_Base):

    def setUp(self):
        self.page = "popout_button.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
        
        expected_result = "foobbaaaahhhrr"
        
        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.5)
        
        click_button('submitfoo',self.browser)
        
        time.sleep(0.5)
        
        p_text = get_p_text('doodah',self.browser)
        
        self.assertEqual(p_text,expected_result)
        
class Test_Popout_Select(Test_Base):

    def setUp(self):
        self.page = "popout_select.php"
        Test_Base.setUp(self,self.page)
        
    def test_1select(self):
        
        expected_result = "http://0.0.0.0/popout_select.php?handle1=out&last_source_value=&ztypes=&&cnstr_subject=NotSelected&cnstr_dow=TU"
        
        click_popupmenu("handle1",self.browser)
        
        set_select_element("cnstr_dow","TU",self.browser)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    '''def test_2select(self):
        
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=Wednesday,Friday&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("Friday",self.browser)
        time.sleep(0.1)
        set_checkbox_element("Wednesday",self.browser)
        time.sleep(0.1)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_dimensions(self):
        
        click_popupmenu("handle1",self.browser)
        
        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,87)
        
    def test_sticky(self):

        click_popupmenu("handle1",self.browser)
    
        time.sleep(0.1)
        execute_script(self.browser, "window.location = 'http://0.0.0.0/"+self.page+"?'+ getAllInputValues('ztypes',['qunit-filter-input']);")
        time.sleep(0.1)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,87)
        
    def test_openclose(self):

        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.5)
        click_popupmenu("handle1",self.browser)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,-83)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,87)'''
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Popout_Mixed(Test_Base):

    def setUp(self):
        self.page = "popout_mixed.php"
        Test_Base.setUp(self,self.page)
        
    def test_1select(self):
        
        expected_result = "http://0.0.0.0/popout_mixed.php?handle1=out&last_source_value=&ztypes=&cnstr_dow=TU&cnstr_period=830-910&cnstr_subject=NotSelected&cnstr_student=Clayton"
        
        click_popupmenu("handle1",self.browser)
        
        set_select_element("cnstr_student","Clayton",self.browser)
        set_checkbox_element("TU",self.browser)
        set_checkbox_element("830-910",self.browser)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    '''def test_2select(self):
        
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=Wednesday,Friday&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("Friday",self.browser)
        time.sleep(0.1)
        set_checkbox_element("Wednesday",self.browser)
        time.sleep(0.1)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_dimensions(self):
        
        click_popupmenu("handle1",self.browser)
        
        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,87)
        
    def test_sticky(self):

        click_popupmenu("handle1",self.browser)
    
        time.sleep(0.1)
        execute_script(self.browser, "window.location = 'http://0.0.0.0/"+self.page+"?'+ getAllInputValues('ztypes',['qunit-filter-input']);")
        time.sleep(0.1)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,87)
        
    def test_openclose(self):

        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.5)
        click_popupmenu("handle1",self.browser)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,-83)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,87)'''
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Table(Test_Base):

    def setUp(self):
        self.page = "table.php"
        Test_Base.setUp(self,self.page)
        
    def test_1select(self):
        
        time.sleep(0.5)

        self.assertTrue(element_exists("//table[@class='borderoff']",self.browser))


    def tearDown(self):
        self.browser.quit()

class Test_Popout_Server(Test_Base):
    
    def setUp(self):
        self.page = "popout_server.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
        
        click_popupmenu("handle1",self.browser)
        
        set_input_text_element('code','foo',self.browser)
        set_input_text_element('name','bar',self.browser)
        
        time.sleep(0.5)
        
        self.assertEqual(get_input_text_element('name',self.browser),'bar')
        self.assertEqual(get_input_text_element('code',self.browser),'foo')
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Popout_JSServer(Test_Base):
    
    def setUp(self):
        self.page = "popout_jsserver.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
        
        click_popupmenu("handle1",self.browser)
        
        set_select_element('objtype','lesson',self.browser)
        
        time.sleep(0.5)
        
        set_select_element('recordtype','subject',self.browser)
        set_select_element('period','830-910',self.browser)
        set_select_element('adult','Stan',self.browser)
        set_select_element('student','Clayton',self.browser)
        set_select_element('subject','Math',self.browser)
        set_select_element('dow','TU',self.browser)
        
        self.assertEqual(get_select_element_value('student',self.browser),'Clayton')
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Popout_JSServerExtCls(Test_Base):
    
    def setUp(self):
        self.page = "popout_jsserverentry_ext_cls.php"
        Test_Base.setUp(self,self.page)
        
    def test_lesson(self):

        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','lesson',self.browser)
        
        time.sleep(0.2)
        
        set_select_element('dow','WE',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(0.2)
        
        self.assertTrue(element_exists("//p[@id='1.3.2.6.22']",self.browser))
        
    def test_subject(self):

        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','subject',self.browser)
        
        time.sleep(0.2)
        
        set_input_text_element('code','mariokarts',self.browser)
        set_input_text_element('name','mariokarts',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(0.2)
        
        self.assertTrue(element_exists("//p[@id='mariokarts']",self.browser))
        
        
    def tearDown(self):
        self.browser.quit()
           
class Test_Popout_JSServerExtCls2p(Test_Base):
    
    def setUp(self):
        self.page = "popout_jsserverentry_ext_cls2p.php"
        Test_Base.setUp(self,self.page)
        
    def test_addlesson(self):
        
        # show pivot

        # for some reason the click is broken on handle1 you 
        # can replicate using browser directly
        #click_popupmenu("handle1",self.browser)
        
        time.sleep(0.2)
        
        # we can however make the selection if not poppped out
        set_select_element('source_value','Clayton',self.browser)
        
        time.sleep(0.2)
        
        # add lesson

        click_popupmenu("handle2",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','lesson',self.browser)
        
        time.sleep(0.2)
        
        set_select_element('dow','WE',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(1)
        
        # scrape the table
        expected_results = [u'Humanities', u'Amelia', u'Humanities', u'Amelia', u'Physics', u'Amelia',u'Math', u'Stan']
        results = get_table_values(self.browser)
        
        self.assertListEqual(expected_results,results)
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Pivot(Test_Base):
    
    def setUp(self):
        self.page = "pivot.php"
        Test_Base.setUp(self,self.page)
        
    def test_drawpivot(self):
        
        #click_popupmenu("handle1",self.browser)
        
        set_select_element('source_value','Clayton',self.browser)
        
        time.sleep(0.5)
    
        results = get_table_values(self.browser)
        
        expected_results = [u'Humanities', u'Amelia', u'Physics', u'Amelia',u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
    def test_drawpivot_3ztypes(self):
        
        #click_popupmenu("handle1",self.browser)
        
        set_select_element('source_value','Clayton',self.browser)

        # set ztypes
        click_popupmenu("handle2",self.browser)        
        set_checkbox_element('student',self.browser)
        set_checkbox_element('period',self.browser)
        set_checkbox_element('adult',self.browser)
        
    
        results = get_table_values(self.browser)
        
        expected_results = [u'Amelia', u'Clayton', u'830-910', u'Amelia', u'Clayton', u'910-950',u'Stan', u'Clayton', u'910-950']
        
        self.assertListEqual(expected_results,results)
        
    def test_drawpivot_filter(self):
        ''' sometimes because the css has changed elsewhere the popouts can
        overlap on the screen and you cant click them programatically so
        easier to not click them open '''
        
        #click_popupmenu("handle1",self.browser)
        
        set_select_element('source_value','Clayton',self.browser)

        # set filters
        #click_popupmenu("handle3",self.browser) 
        
        set_checkbox_element('WE',self.browser)
        
        # set ztypes
        click_popupmenu("handle2",self.browser)        
        set_checkbox_element('student',self.browser)
        set_checkbox_element('period',self.browser)
        set_checkbox_element('adult',self.browser)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'Stan', u'Clayton', u'910-950']
        
        self.assertListEqual(expected_results,results)
    def tearDown(self):
        self.browser.quit()
        
class Test_Menu(Test_Base):
    
    def setUp(self):
        self.page = "menu.php"
        Test_Base.setUp(self,self.page)
        
    def test_hyperlink(self):
        
        expected_result = "http://0.0.0.0/foobar.php"
        
        contextclick_element("mytd",self.browser)
        
        time.sleep(0.2)
        
        click_menu_element("",self.browser,"//a[@id='linka']")
        
        time.sleep(0.2)
        
        self.assertEqual(self.browser.current_url,expected_result)
        
    def test_jscript(self):
        
        expected_result = "http://0.0.0.0/foobar.php"
        
        contextclick_element("mytd",self.browser)
        
        time.sleep(0.2)
        
        click_menu_element("",self.browser,"//a[@id='linkb']")
        
        time.sleep(0.2)
        
        self.assertEqual(self.browser.current_url,expected_result)
        
    def tearDown(self):
        self.browser.quit()
        
class Test_MenuUpdate(Test_Base):
    
    def setUp(self):
        self.page = "popout_menu_update.php"
        Test_Base.setUp(self,self.page)
        
    def test_hyperlink(self):
        
        expected_result = "http://0.0.0.0/foobar.php"
        
        contextclick_element("mytd",self.browser)
        
        time.sleep(0.2)
        
        click_menu_element("",self.browser,"//a[@id='linka']")
        
        time.sleep(0.2)
        
        self.assertEqual(self.browser.current_url,expected_result)
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Edit(Test_Base):
    
    def setUp(self):
        self.page = "popout_edit.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
        
        click_popupmenu("handle1",self.browser)
        
        set_input_text_element("edit_source_value","054C4D26",self.browser,returnkey=True)
        time.sleep(0.2)
        
        set_select_element('subject','Math',self.browser)
        
        time.sleep(0.2)
        
        click_button('editsubmit',self.browser)
        
        time.sleep(0.2)
        
        self.assertTrue(element_exists("//p[@id='1.2.2.6.22']",self.browser))
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Menu_Update(Test_Base):
    
    def setUp(self):
        self.page = "popout_menu_update.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
        
        #click_popupmenu("handle1",self.browser)

        contextclick_element("mytd",self.browser)
        
        time.sleep(0.2)
        
        click_menu_element("",self.browser,"//a[@id='mytd']")
        
        time.sleep(0.2)
        
        set_select_element('dow','TU',self.browser)
        
        time.sleep(0.2)
        
        click_button('editsubmit',self.browser)
        
        time.sleep(0.2)
        
        self.assertTrue(element_exists("//p[@id='1.2.3.4.5']",self.browser))
        
    def tearDown(self):
        self.browser.quit()
        
class Test_PHP_bridge(Test_Base):
    
    def setUp(self):
        self.page = "phpbridge.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
        self.assertTrue(element_exists("//p[@id='bar']",self.browser))
        
    def tearDown(self):
        self.browser.quit()  
        
class Test_Mixed(Test_Base):
    
    def setUp(self):
        self.page = "popout_server_mixed.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
        
        # edit 
        
        click_popupmenu("handle1",self.browser)
        
        set_input_text_element("edit_source_value","02B1EEDC",self.browser,returnkey=True)
        time.sleep(0.2)
        
        set_select_element('subject','Humanities',self.browser)
        
        time.sleep(0.2)
        
        click_button('editsubmit',self.browser)
        
        time.sleep(0.2)
        
        self.assertTrue(element_exists("//p[@id='1.2.3.4.5']",self.browser))
        
        click_popupmenu("handle2",self.browser)
        
        time.sleep(0.2)
        
        # new lesson
        set_select_element('objtype','lesson',self.browser)
        
        time.sleep(0.2)
        
        set_select_element('dow','WE',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(0.2)
        
        self.assertTrue(element_exists("//p[@id='1.3.2.6.22']",self.browser))

        # new subject
        #click_popupmenu("handle2",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','subject',self.browser)
        
        time.sleep(0.2)
        
        set_input_text_element('code','mariokarts',self.browser)
        set_input_text_element('name','mariokarts',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(0.2)
        
        self.assertTrue(element_exists("//p[@id='mariokarts']",self.browser))
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Mixed_wpivot(Test_Base):
    
    def setUp(self):
        self.page = "popout_server_mixed_wpivot.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
                
        # edit

        click_popupmenu("handle2",self.browser)
        
        set_input_text_element("edit_source_value","054C4D26",self.browser,returnkey=True)
        time.sleep(0.2)
        
        set_select_element('subject','Math',self.browser)
        
        time.sleep(0.2)
        
        click_button('editsubmit',self.browser)
        
        time.sleep(0.5)
        
        # pivot
        #click_popupmenu("handle1",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('source_value','Clayton',self.browser)
        
        time.sleep(0.2)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'Math', u'Amelia', u'Physics', u'Amelia', u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
        # new subject
        click_popupmenu("handle3",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','subject',self.browser)
        
        time.sleep(0.2)
        
        set_input_text_element('code','foobar',self.browser)
        set_input_text_element('name','foobar',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        # new lesson
        time.sleep(0.2)
        
        #click_popupmenu("handle3",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','lesson',self.browser)
        
        time.sleep(0.2)
        
        set_select_element('subject','foobar',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(0.5)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'Math', u'Amelia', u'foobar', u'Amelia', u'Physics', u'Amelia', u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
class Test_Mixed_wpivot_crit(Test_Base):
    
    def setUp(self):
        self.page = "popout_server_mixed_wpivot_crit.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
                
        # edit

        click_popupmenu("handle2",self.browser)
        
        set_input_text_element("edit_source_value","054C4D26",self.browser,returnkey=True)
        time.sleep(0.2)
        
        set_select_element('subject','Math',self.browser)
        
        time.sleep(0.2)
        
        click_button('editsubmit',self.browser)
        
        time.sleep(0.5)
        
        # pivot
        #click_popupmenu("handle1",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('source_value','Clayton',self.browser)
        
        time.sleep(0.2)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'Math', u'Amelia', u'Physics', u'Amelia', u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
        # new subject
        click_popupmenu("handle3",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','subject',self.browser)
        
        time.sleep(0.2)
        
        set_input_text_element('code','foobar',self.browser)
        set_input_text_element('name','foobar',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        # new lesson
        time.sleep(0.2)
        
        #click_popupmenu("handle3",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','lesson',self.browser)
        
        time.sleep(0.2)
        
        set_select_element('subject','foobar',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(0.5)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'Math', u'Amelia', u'foobar', u'Amelia', u'Physics', u'Amelia', u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
        # change ztypes / data shown
        
        click_popupmenu("handle5",self.browser)
        
        set_checkbox_element("recordtype",self.browser)
        set_checkbox_element("adult",self.browser)
        set_checkbox_element("subject",self.browser)
        set_checkbox_element("student",self.browser)
        
        results = get_table_values(self.browser)       
        expected_result = [u'Math', u'Amelia', u'Clayton', u'wp', u'foobar', u'Amelia', u'Clayton', u'subject', u'Physics', u'Amelia', u'Clayton', u'academic',u'Math', u'Stan', u'Clayton', u'academic']
            
        self.assertEqual(expected_result,results)
        
        # and then filter
        
        click_popupmenu("handle4",self.browser)
        
        set_checkbox_element("TU",self.browser)
        
        results = get_table_values(self.browser)
        
        expected_result = [u'Math', u'Amelia', u'Clayton', u'wp', u'foobar', u'Amelia', u'Clayton', u'subject', u'Physics', u'Amelia', u'Clayton', u'academic']
        
        self.assertEqual(expected_result,results)
        
    def tearDown(self):
        self.browser.quit()
 
class Test_Mixed_wpivot_crit_menu_update(Test_Base):
    
    def setUp(self):
        self.page = "popout_server_mixed_wpivot_crit.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
                
        # edit

        time.sleep(0.2)
        
        set_select_element('source_value','Clayton',self.browser)
        
        time.sleep(0.2)

        set_checkbox_element("id",self.browser)
        
        time.sleep(0.2)
        
        contextclick_element("1.1.0",self.browser)
        
        time.sleep(0.2)
        
        click_menu_element("",self.browser,"//a[@id='1.1.0']")
        
        time.sleep(0.2)
        
        
    def tearDown(self):
        self.browser.quit()
        
class Test_View(Test_Base):
    
    def setUp(self):
        self.page = "view.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
                
        
        click_popupmenu("handle1",self.browser)
        
        # list
        time.sleep(0.2)
        set_select_element('view_type','list',self.browser)
        
        time.sleep(0.2)

        click_button('viewsubmit',self.browser)
        
        time.sleep(1)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'status', u'substatus', u'recordtype', u'period', u'dow', u'source', u'session', u'adult', u'student', u'id', u'objtype', u'prep', u'userobjid', u'subject', u'master', u'complete', u'wp', u'830-910', u'TU', u'dbinsert', u'Amelia.Humanities.Tuesday.830-910', u'Amelia', u'Clayton', u'054C4D26', u'lesson', u'5', u'1.2.2.6.22', u'Humanities', u'master', u'complete', u'academic', u'910-950', u'WE', u'dbinsert', u'Stan.Math.Wednesday.910-950', u'Stan', u'Clayton', u'02B1EEDC', u'lesson', u'5', u'1.2.3.4.5', u'Math', u'master', u'complete', u'academic', u'910-950', u'TU', u'dbinsert', u'Amelia.Physics.TU.910-950', u'Amelia', u'Clayton', u'00FE6F46', u'lesson', u'5', u'1.2.3.6.33', u'Physics']
        
        self.assertListEqual(expected_results,results)
        
        # pivot
        time.sleep(0.2)
        set_select_element('view_type','pivot',self.browser)
        
        time.sleep(0.2)

        set_select_element('yaxis','dow',self.browser)
        
        time.sleep(0.5)
        
        set_select_element('source_type','adult',self.browser)
        time.sleep(0.5)
        set_select_element('source_type','student',self.browser)
        
        time.sleep(0.5)  
        
        set_select_element('source_value','Clayton',self.browser)
    
        click_button('viewsubmit',self.browser)        
        
        time.sleep(0.5)
        results = get_table_values(self.browser)
        
        expected_results = [u'Humanities', u'Amelia', u'Physics', u'Amelia', u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
class Test_Mixed_wpivot_crit(Test_Base):
    
    def setUp(self):
        self.page = "popout_server_mixed_wpivot_crit.php"
        Test_Base.setUp(self,self.page)
        
    def test_(self):
                
        # edit

        click_popupmenu("handle2",self.browser)
        
        set_input_text_element("edit_source_value","054C4D26",self.browser,returnkey=True)
        time.sleep(0.2)
        
        set_select_element('subject','Math',self.browser)
        
        time.sleep(0.2)
        
        click_button('editsubmit',self.browser)
        
        time.sleep(0.5)
        
        # pivot
        #click_popupmenu("handle1",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('source_value','Clayton',self.browser)
        
        time.sleep(0.2)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'Math', u'Amelia', u'Physics', u'Amelia', u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
        # new subject
        click_popupmenu("handle3",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','subject',self.browser)
        
        time.sleep(0.2)
        
        set_input_text_element('code','foobar',self.browser)
        set_input_text_element('name','foobar',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        # new lesson
        time.sleep(0.2)
        
        #click_popupmenu("handle3",self.browser)
        
        time.sleep(0.2)
        
        set_select_element('objtype','lesson',self.browser)
        
        time.sleep(0.2)
        
        set_select_element('subject','foobar',self.browser)
        
        time.sleep(0.2)
        
        click_button('newsubmit',self.browser)
        
        time.sleep(0.5)
        
        results = get_table_values(self.browser)
        
        expected_results = [u'Math', u'Amelia', u'foobar', u'Amelia', u'Physics', u'Amelia', u'Math', u'Stan']
        
        self.assertListEqual(expected_results,results)
        
        # change ztypes / data shown
        
        click_popupmenu("handle5",self.browser)
        
        set_checkbox_element("recordtype",self.browser)
        set_checkbox_element("adult",self.browser)
        set_checkbox_element("subject",self.browser)
        set_checkbox_element("student",self.browser)
        
        results = get_table_values(self.browser)       
        expected_result = [u'Math', u'Amelia', u'Clayton', u'wp', u'foobar', u'Amelia', u'Clayton', u'subject', u'Physics', u'Amelia', u'Clayton', u'academic',u'Math', u'Stan', u'Clayton', u'academic']
            
        self.assertEqual(expected_result,results)
        
        # and then filter
        
        click_popupmenu("handle4",self.browser)
        
        set_checkbox_element("TU",self.browser)
        
        results = get_table_values(self.browser)
        
        expected_result = [u'Math', u'Amelia', u'Clayton', u'wp', u'foobar', u'Amelia', u'Clayton', u'subject', u'Physics', u'Amelia', u'Clayton', u'academic']
        
        self.assertEqual(expected_result,results)
        
    def tearDown(self):
        self.browser.quit()
        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pivot))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_MultiSelect_DOW))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_MultiSelect_DOW_Period))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_Select))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_Mixed))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Table))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_JSButton))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_Server))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_JSServer))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_JSServerExtCls))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_JSServerExtCls2p))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Menu))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PHP_bridge))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Menu_Update))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Mixed))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Mixed_wpivot))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Mixed_wpivot_crit))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Mixed_wpivot_crit_menu_update))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Edit))'''
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Mixed_wpivot_crit))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_View))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 