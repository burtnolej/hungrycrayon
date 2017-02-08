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

baseurl = "http://0.0.0.0"

class Test_Base(unittest.TestCase):
    
    def setUp(self,page):
    
        self.browser = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)    

        _url = [baseurl,page]
        self.url = "/".join(_url)
        self.browser.get(self.url)
        
class Test_Popout_DOW(Test_Base):

    def setUp(self):
        self.page = "popout_dow.php"
        Test_Base.setUp(self,self.page)
        
    def test_1select(self):
        
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=Friday&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("Friday",self.browser)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_2select(self):
        
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
        self.assertAlmostEqual(h,87)
        
    def tearDown(self):
        self.browser.quit()
        
class Test_Popout_DOW_Period(Test_Base):

    def setUp(self):
        self.page = "popout_dow_period.php"
        Test_Base.setUp(self,self.page)
        
    def test_1select(self):
                
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=Monday&cnstr_period=830-910&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("830-910",self.browser)
        set_checkbox_element("Monday",self.browser)
            
        self.assertEqual(expected_result,self.browser.current_url)
        
    def test_2select(self):
        
        expected_result = "http://0.0.0.0/"+self.page+"?handle1=out&last_source_value=&ztypes=&cnstr_dow=Wednesday,Friday&cnstr_period=830-910,910-950&"
        
        click_popupmenu("handle1",self.browser)
        
        set_checkbox_element("830-910",self.browser)        
        time.sleep(0.1)
        set_checkbox_element("Friday",self.browser)
        time.sleep(0.1)
        set_checkbox_element("910-950",self.browser)     
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
        self.assertAlmostEqual(h,211)
        
    def test_sticky(self):

        click_popupmenu("handle1",self.browser)
    
        time.sleep(0.1)
        execute_script(self.browser, "window.location = 'http://0.0.0.0/"+self.page+"?'+ getAllInputValues('ztypes',['qunit-filter-input']);")
        time.sleep(0.1)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,1)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,211)
        
    def test_openclose(self):

        click_popupmenu("handle1",self.browser)
        
        time.sleep(0.5)
        click_popupmenu("handle1",self.browser)

        x,y,w,h = get_dimensions('',self.browser,"//div[contains(@class,'slide-out1')]")
        
        self.assertAlmostEqual(x,604)
        self.assertAlmostEqual(y,-207)
        self.assertAlmostEqual(w,308)
        self.assertAlmostEqual(h,211)
        
    def tearDown(self):
        self.browser.quit()
        

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_DOW))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Popout_DOW_Period))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 