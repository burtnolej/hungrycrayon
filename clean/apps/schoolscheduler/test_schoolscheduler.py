import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from schoolscheduler import _initdatamembers, _enrich, schedule_load, _lesson_create
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory
from schoolscheduler_defn import *
from schoolscheduler_htmlparser import *

import unittest

[[['Period', 'Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
  ['1', '8:30- 9:10', 'Movement', 'Movement', 'Chess With: Rahul', 'Core', 'Stem'], 
  ['2', '9:11- 9:51', 'YOGA', 'Art', 'Reading Period With: Nathaniel', 'Science', 'Movement']]]


def _pprint(obj1,obj2):
    from pprint import pprint
    pprint(obj1)
    pprint(obj2)
    
class Test_SchoolSched_enrich(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_breakperiod(self):
        # dow starts from 2/Monday thru 7
        datamembers = _initdatamembers(1,2,2)
        _enrich('QUAD CAFE',datamembers)
        
        exp_res = {'teacher':None,
                   'subject':'QUAD CAFE',
                   'lessontype':'break',
                   'period':'9:11-9:51',
                   'dow':'Monday',
                   'objid':'1.0.1'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_psychperiod(self):
        datamembers = _initdatamembers(1,4,8)
        _enrich('COUNSELING',datamembers)
        
        exp_res = {'teacher':None,
                   'subject':'COUNSELING',
                   'lessontype':'psych',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'objid':'1.2.7'}  

        self.assertEquals(exp_res,datamembers)
        

    def test_eduperiod(self):
        datamembers = _initdatamembers(1,6,10)
        _enrich('HUMANITIES',datamembers)
        
        exp_res = {'teacher':None,
                   'subject':'HUMANITIES',
                   'lessontype':'edu',
                   'period':'2:30-3:00',
                   'dow':'Friday',
                   'objid':'1.4.9'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_otherperiod(self):
        datamembers = _initdatamembers(1,4,8)
        _enrich('CODING/TED TALKS',datamembers)
        
        exp_res = {'teacher':None,
                   'subject':'CODING/TED TALKS',
                   'lessontype':'other',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'objid':'1.2.7'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_workperiod(self):
        datamembers = _initdatamembers(1,4,8)
        _enrich('Math WP With: Moira',datamembers)
        
        exp_res = {'teacher':'Moira',
                   'subject':'Math',
                   'lessontype':'wp',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'objid':'1.2.7'} 

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_workperiod_wp(self):
        # 'wp' tag used not 'work period'
        datamembers = _initdatamembers(1,4,8)
        _enrich('Science WP With: Kayla',datamembers)
        
        exp_res = {'teacher':'Kayla',
                   'subject':'Science',
                   'lessontype':'wp',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'objid':'1.2.7'} 

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod(self):
        # work period with no subject specified
        datamembers = _initdatamembers(1,5,5)
        _enrich('Work Period With: Rachel',datamembers)
        
        exp_res = {'teacher':'Rachel',
                   'subject':None,
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'objid':'1.3.4'} 

        #_pprint(exp_res,datamembers)
        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_2_teachers(self):
        # work period and 2 teachers
        datamembers = _initdatamembers(1,5,5)
        _enrich('Work Period with Ashley With: Dylan',datamembers)
        
        exp_res = {'teacher':'Dylan',
                   'subject':None,
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'objid':'1.3.4'} 

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_noteacher(self):
        # work period and nothing else
        datamembers = _initdatamembers(1,5,5)
        _enrich('Work Period',datamembers)
        
        exp_res = {'teacher':None,
                   'subject':None,
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'objid':'1.3.4'} 

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_backslash(self):
        # work period and W/
        datamembers = _initdatamembers(1,5,5)
        _enrich('Work Period W/ Rahul',datamembers)
        
        exp_res = {'teacher':'Rahul',
                   'subject':None,
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'objid':'1.3.4'} 

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_nowith(self):
        # work period and just teacher name
        datamembers = _initdatamembers(1,5,5)
        _enrich('Work Period Alexa',datamembers)
        
        exp_res = {'teacher':'Alexa',
                   'subject':None,
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'objid':'1.3.4'} 

        self.assertEquals(exp_res,datamembers)

    def test_edu_nonworkperiod_noteacher2(self):
        # work period captial W small p nothing else
        datamembers = _initdatamembers(1,5,5)
        _enrich('Work period',datamembers)
        
        exp_res = {'teacher':None,
                   'subject':None,
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'objid':'1.3.4'} 

        self.assertEquals(exp_res,datamembers)
        
    def test_no_match(self):
        # work period and just teacher name
        datamembers = _initdatamembers(1,5,5)
        
        with self.assertRaises(Exception):
            _enrich('Regions Prep',datamembers)
        

class Test_SchoolSched_completeness(unittest.TestCase):
    
    def test_completeness(self):
        
        schedule, students = htmlschedule_parse('schedule.html')
        
        schedule_load(schedule)
       
       
class Test_SchoolSched_lesson_create(unittest.TestCase):
    
    # test that a lesson object is created properly by asserting
    # the existence and values of each of its attributes

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_(self):
        datamembers = {'objtype':'lesson',
                       'teacher':'Rahul',
                       'subject':'QUAD CAFE',
                       'lessontype':'break',
                       'period':'9:11-9:51',
                       'dow':'Monday',
                       'userdefid':'1.0.1',
                       'student':'BOOKER'}
        
        exp_res=[('objtype','lesson'),
                 ('dow','Monday'),
                 ('teacher','Rahul'),
                 ('subject','QUAD CAFE'),
                 ('lessontype','break'),
                 ('period','9:11-9:51'),
                 ('userdefid','1.0.1'),
                 ('student','BOOKER')]
        
        exp_res.sort()
        
        lesson = _lesson_create(datamembers,self.database,self.of)
        
        attr = lesson.attr_get_keyval(include_callable=False,
                                          include_nondataattr=False)
            
        attr.sort()
        
        self.assertEquals(attr,exp_res)
        
class Test_SchoolSched_create_secondary_objects(unittest.TestCase):
    
    # test that when a lesson object is created, all other records
    # that are new are created by asserting the contents of the
    # objfactory store

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_(self):
        datamembers = {'objtype':'lesson',
                       'teacher':'Rahul',
                       'subject':'QUAD CAFE',
                       'lessontype':'break',
                       'period':'9:11-9:51',
                       'dow':'Monday',
                       'userdefid':'1.0.1',
                       'student':'BOOKER'}
        
    
        exp_res = [('Rahul','teacher'),
                   ('9:11-9:51','period'),
                   ('BOOKER','student'),
                   ('Monday','dow'),
                   ('lesson','objtype'),
                   ('1.0.1','lesson'),
                   ('1.0.1','userdefid'),
                   ('break','lessontype'),
                   ('QUAD CAFE','subject')]


        _lesson_create(datamembers,self.database,self.of)

        attr_list = [(obj.userdefid, obj.objtype) for obj in self.of.object_iter()]

        attr_list.sort()
        exp_res.sort()
        
        #_pprint(exp_res,attr_list)
        self.assertListEqual(attr_list,exp_res)
        
class Test_SchoolSched_create_secondary_objects_type(unittest.TestCase):
    
    # test that when a lesson object is created, all other records
    # that are new are created by asserting that the values are of
    # the correct object type

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_(self):
        datamembers = {'objtype':'lesson',
                       'teacher':'Rahul',
                       'subject':'QUAD CAFE',
                       'lessontype':'break',
                       'period':'9:11-9:51',
                       'dow':'Monday',
                       'userdefid':'1.0.1',
                       'student':'BOOKER'}

        _lesson_create(datamembers,self.database,self.of)

        attr_list = [(obj, obj.objtype) for obj in self.of.object_iter()]

        for obj in self.of.object_iter():
            self.assertTrue(isinstance(obj,eval(obj.objtype)))

class Test_SchoolSched_persist(unittest.TestCase):

    # test that a lesson object is persisted to the db correctly
    # by asserting the fields written into the database table
    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_persist_lesson(self):
        datamembers = {'teacher':'Rahul',
                       'subject':'QUAD CAFE',
                       'lessontype':'break',
                       'period':'9:11-9:51',
                       'dow':'Monday',
                       'userdefid':'1.0.1',
                       'student':'BOOKER'}
        
        lesson = _lesson_create(datamembers,self.database,self.of)
        with self.database:
            lesson.persist()
            
        self.database = Database('htmlparser',True)
        with self.database:
            colnames,rowvals =  tbl_rows_get(self.database,'lesson',datamembers.keys())
    
        
        rowvals = [str(val) for val in rowvals[0]]
        rowvals.sort()
        
        exp_res = datamembers.values()
        exp_res.sort()
        
        self.assertListEqual(rowvals,exp_res)

class Test_SchoolSched_persist_secondary(unittest.TestCase):

    # test that a the secondary objects are persisted to the db correctly
    # by asserting the fields written into the database table
    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_persist_lesson(self):
        datamembers = {'teacher':'Rahul',
                       'subject':'QUAD CAFE',
                       'lessontype':'break',
                       'period':'9:11-9:51',
                       'dow':'Monday',
                       'userdefid':'1.0.1',
                       'student':'BOOKER'}
        
        _lesson_create(datamembers,self.database,self.of)
        with self.database:
            for obj in self.of.object_iter():
                obj.persist()
            
        self.database = Database('htmlparser',True)
        res = {}
        with self.database:
            for tblname,userdefidval in datamembers.iteritems():
                _,rowvals =  tbl_rows_get(self.database,tblname,['userdefid'])
                res[tblname] = rowvals[0][0]
        
        self.assertEqual(res,datamembers)
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_enrich))  
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_completeness))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_lesson_create))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_create_secondary_objects))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_create_secondary_objects_type))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_persist))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_persist_secondary))

    
    
    unittest.TextTestRunner(verbosity=2).run(suite)