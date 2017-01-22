import unittest

from misc_utils_selenium import *

# java -jar selenium-server-standalone-2.53.0.jar -Dwebdriver.gecko.driver=/usr/local/bin/geckodriver

import os
import time

#baseurl = "http://www.hungrycrayon.com"
#baseurl = "http://192.168.1.254"
baseurl = "http://0.0.0.0"
page="dpivot.php"


'''
fucia.sqlite -> ../apps/schoolschedulewizard/test_multi.sqlite
python ./ssviewer_rest.py --allow-unknown
java -jar selenium-server-standalone-2.53.0.jar -Dwebdriver.gecko.driver=/usr/local/bin/geckodriver

run selenium-reset-multi.sh 

'''      
    
class Test_Base(unittest.TestCase):
    
    def setUp(self):
    
        self.browser = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)    

        _url = [baseurl,page]
        self.url = "/".join(_url)
        self.browser.get(self.url)
      

class Test_Add(Test_Base):

    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        expected_results = [u'status', u'prep', u'recordtype', u'period', u'substatus', u'source', u'session', u'adult', u'student', u'objtype', u'dow', u'userobjid', u'subject', 
                            u'master', u'5', u'academic', u'830-910', u'complete', u'manual', u'Stan.Math.MO.830-910', u'Stan', u'Clayton', u'lesson', u'MO', u'1.1.None.2.2', u'Math', 
                            u'master', u'5', u'academic', u'910-950', u'complete', u'manual', u'Amelia.Humanities.MO.910-950', u'Amelia', u'Clayton', u'lesson', u'MO', u'2.1.None.None.None', u'Humanities', 
                            u'master', u'5', u'academic', u'830-910', u'complete', u'manual', u'Amelia.Humanities.TU.830-910', u'Amelia', u'Clayton', u'lesson', u'TU', u'1.2.None.None.None', u'Humanities', 
                            u'master', u'5', u'academic', u'910-950', u'complete', u'manual', u'Stan.Math.TU.910-950', u'Stan', u'Clayton', u'lesson', u'TU', u'2.2.None.2.2', u'Math', 
                            u'master', u'5', u'academic', u'910-950', u'complete', u'manual', u'Stan.Math.MO.910-950', u'Stan', u'Nathaniel', u'lesson', u'MO', u'2.1.2.2.2', u'Math', 
                            u'master', u'5', u'academic', u'830-910', u'complete', u'manual', u'Amelia.Humanities.MO.830-910', u'Amelia', u'Nathaniel', u'lesson', u'MO', u'1.1.2.None.None', u'Humanities', 
                            u'master', u'5', u'academic', u'910-950', u'complete', u'manual', u'Amelia.Humanities.TU.910-950', u'Amelia', u'Nathaniel', u'lesson', u'TU', u'2.2.2.None.None', u'Humanities', 
                            u'master', u'5', u'academic', u'830-910', u'complete', u'manual', u'Stan.Math.TU.830-910', u'Stan', u'Nathaniel', u'lesson', u'TU', u'1.2.2.2.2', u'Math']
        
        
                
        values = dict(period=[dict(name='830-910',code='830-910'),
                              dict(name='910-950',code='910-950'),
                              dict(name='950-1030',code='950-1030'),
                              dict(name='1030-1110',code='1030-1110')                              ],
                      dow=[dict(name='MO',code='MO'),
                           dict(name='TU',code='TU'),
                           dict(name='WE',code='WE'),
                           dict(name='TH',code='TH')],
                      recordtype=[dict(name="academic",code="AC"),
                                  dict(name="workperiod",code="WP")],
                      student=[dict(name="Clayton",code="CLAY",prep='5'),
                               dict(name="Nathaniel",code="NATH",prep='5')],
                      adult=[dict(name="Amelia",code="AMEL"),
                             dict(name="Stan",code="STAN")],
                      subject=[dict(name="Humanities",code="HUMN"),
                               dict(name="Math",code="MATH")])
        
        
        for objtype,vlist in values.iteritems():
            for v in vlist:
                _macro_add_new_record(self.browser,objtype,v)
        
        time.sleep(0.2)
        
        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="830-910",
                                                         teacher="Stan", 
                                                         student="Clayton",
                                                         dow="MO",
                                                         subject="Math"))
        
        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="910-950",
                                                         teacher="Amelia", 
                                                         student="Clayton",
                                                         dow="MO",
                                                         subject="Humanities"))

        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="830-910",
                                                         teacher="Amelia", 
                                                         student="Clayton",
                                                         dow="TU",
                                                         subject="Humanities"))
        
        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="910-950",
                                                         teacher="Stan", 
                                                         student="Clayton",
                                                         dow="TU",
                                                         subject="Math"))
        
        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="910-950",
                                                         teacher="Stan", 
                                                         student="Nathaniel",
                                                         dow="MO",
                                                         subject="Math"))
        
        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="830-910",
                                                         teacher="Amelia", 
                                                         student="Nathaniel",
                                                         dow="MO",
                                                         subject="Humanities"))

        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="910-950",
                                                         teacher="Amelia", 
                                                         student="Nathaniel",
                                                         dow="TU",
                                                         subject="Humanities"))
        
        _macro_add_new_record(self.browser,"lesson",dict(recordtype="academic",
                                                         period="830-910",
                                                         teacher="Stan", 
                                                         student="Nathaniel",
                                                         dow="TU",
                                                         subject="Math"))
        

        
        
        _macro_list_objects(self.browser,"lesson")
    
        sleeptime=0.1
        results = get_table_values(self.browser,suppressid=True)
        self.assertListEqual(results,expected_results)     
        
        
        # check the pivot
        
        expected_results = [u'Math', u'Stan', u'Clayton', u'830-910', u'MO', 
                            u'Humanities', u'Amelia', u'Nathaniel', u'830-910', u'MO', 
                            u'Humanities', u'Amelia', u'Clayton', u'830-910', u'TU', 
                            u'Math', u'Stan', u'Nathaniel', u'830-910', u'TU', 
                            u'Humanities', u'Amelia', u'Clayton', u'910-950', u'MO', 
                            u'Math', u'Stan', u'Nathaniel', u'910-950', u'MO', 
                            u'Math', u'Stan', u'Clayton', u'910-950', u'TU', 
                            u'Humanities', u'Amelia', u'Nathaniel', u'910-950', u'TU']
        
        _macro_do_pivot(self.browser,'student','all',['subject','adult',
                                                      'student','dow',
                                                      'period'])
        
        sleeptime=0.1
        results = get_table_values(self.browser)
        self.assertListEqual(results,expected_results)   
        
    def tearDown(self):
        self.browser.quit()
             
class Test_Update(Test_Base):

    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        # ##################################################
        # update_all_MO_to_WE_and_TU_to_TH(self):
        
        expected_results = [u'Math', u'Stan', u'Clayton', u'830-910', u'WE', 
                            u'Humanities', u'Amelia', u'Nathaniel', u'830-910', u'WE', 
                            u'Humanities', u'Amelia', u'Clayton', u'830-910', u'TH', 
                            u'Math', u'Stan', u'Nathaniel', u'830-910', u'TH', 
                            u'Humanities', u'Amelia', u'Clayton', u'910-950', u'WE', 
                            u'Math', u'Stan', u'Nathaniel', u'910-950', u'WE', 
                            u'Math', u'Stan', u'Clayton', u'910-950', u'TH', 
                            u'Humanities', u'Amelia', u'Nathaniel', u'910-950', u'TH']
        sleeptime=0.1
        
        # update MO to WE
        _macro_list_objects(self.browser,"lesson",dict(dow='MO'))
    
        # get ID's of the records we want to update
        ids = get_table_values(self.browser,onlyid=True)
    
        for i in range(1,len(ids)):
            _macro_update_field(self.browser,ids[i],dict(dow="WE"))
            
        # update TU to TH
        _macro_list_objects(self.browser,"lesson",dict(dow='TU'))
    
        ids = get_table_values(self.browser,onlyid=True)
    
        for i in range(1,len(ids)):
            _macro_update_field(self.browser,ids[i],dict(dow="TH"))
            
        # get pivot
        _macro_do_pivot(self.browser,'student','all',['subject','adult',
                                                      'student','dow',
                                                      'period'])
        
        results = get_table_values(self.browser)

        self.assertListEqual(results,expected_results)
        
        # ##################################################
        # update_all_830_to_950_and_910_to_1030(self):
        #
        
        expected_results = [u'Math', u'Stan', u'Clayton', u'950-1030', u'WE', 
                            u'Humanities', u'Amelia', u'Nathaniel', u'950-1030', u'WE', 
                            u'Humanities', u'Amelia', u'Clayton', u'950-1030', u'TH', 
                            u'Math', u'Stan', u'Nathaniel', u'950-1030', u'TH', 
                            u'Humanities', u'Amelia', u'Clayton', u'1030-1110', u'WE', 
                            u'Math', u'Stan', u'Nathaniel', u'1030-1110', u'WE', 
                            u'Math', u'Stan', u'Clayton', u'1030-1110', u'TH', 
                            u'Humanities', u'Amelia', u'Nathaniel', u'1030-1110', u'TH']
        sleeptime=0.1
        
        # update MO to WE
        _macro_list_objects(self.browser,"lesson",dict(period='830-910'))
    
        # get ID's of the records we want to update
        ids = get_table_values(self.browser,onlyid=True)
    
        for i in range(1,len(ids)):
            _macro_update_field(self.browser,ids[i],dict(period="950-1030"))
            
        # update TU to TH
        _macro_list_objects(self.browser,"lesson",dict(period='910-950'))
    
        ids = get_table_values(self.browser,onlyid=True)
    
        for i in range(1,len(ids)):
            _macro_update_field(self.browser,ids[i],dict(period="1030-1110"))
            
        # get pivot
        _macro_do_pivot(self.browser,'student','all',['subject','adult',
                                                      'student','dow',
                                                      'period'])
        
        results = get_table_values(self.browser)

        self.assertListEqual(results,expected_results)

        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Update))
    unittest.TextTestRunner(verbosity=2).run(suite) 