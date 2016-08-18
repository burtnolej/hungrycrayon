import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from schoolscheduler import _initdatamembers, _enrich, schedule_load, _lesson_create, \
     schedule_persist, _token_type_get, _validate_token
from database_util import Database, tbl_count_get
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory
#from schoolscheduler_defn import *
from schoolscheduler_htmlparser import *
from schoolscheduler_utils import *

import unittest

def _pprint(obj1,obj2):
    from pprint import pprint
    pprint(obj1)
    pprint(obj2)
    
def _cdict(keys,vals):
    ''' simple func to create a dict from 2 arrays to make it easier to 
    change the test variables in each of the tests as only the 2nd array needs to change'''
    d={}
    for i in range(len(keys)):
        d[keys[i]] = vals[i]
    return(d)
        
class Test_SchoolSched_enrich(unittest.TestCase):

    def setUp(self):
        pass

        
    def test_breakperiod(self):
        # dow starts from 2/Monday thru 7
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,0,1,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('QUAD CAFE',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'QUAD CAFE',
                   'lessontype':'break',
                   'period':'9:11-9:51',
                   'dow':'Monday',
                   'userdefid':'1.0.1',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_psychperiod(self):        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,2,7,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('COUNSELING',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'COUNSELING',
                   'lessontype':'psych',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'userdefid':'1.2.7',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        

    def test_eduperiod(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,4,9,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('HUMANITIES',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'HUMANITIES',
                   'lessontype':'edu',
                   'period':'2:30-3:00',
                   'dow':'Friday',
                   'userdefid':'1.4.9',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  
    

        self.assertEquals(exp_res,datamembers)
        
    def test_otherperiod(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,2,7,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('CODING/TED TALKS',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'CODING/TED TALKS',
                   'lessontype':'other',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'userdefid':'1.2.7',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_workperiod(self):

        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,2,7,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Math WP With: Moira',datamembers)
        
        exp_res = {'teacher':'MOIRA',
                   'subject':'MATH',
                   'lessontype':'wp',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'userdefid':'1.2.7',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_workperiod_wp(self):
        # 'wp' tag used not 'work period'
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,2,7,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Science WP With: Kayla',datamembers)
        
        exp_res = {'teacher':'KAYLA',
                   'subject':'SCIENCE',
                   'lessontype':'wp',
                   'period':'1:07-1:47',
                   'dow':'Wednesday',
                   'userdefid':'1.2.7',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod(self):
        # work period with no subject specified
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Work Period With: Rachel',datamembers)
        
        exp_res = {'teacher':'RACHEL',
                   'subject':'None',
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        #_pprint(exp_res,datamembers)
        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_ex2(self):
        # work period with no subject specified
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Chess With: Rahul',datamembers)
        
        exp_res = {'teacher':'RAHUL',
                   'subject':'CHESS',
                   'lessontype':'break',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        #_pprint(exp_res,datamembers)
        self.assertEquals(exp_res,datamembers)
        


        
    def test_edu_nonworkperiod_2_teachers(self):
        # work period and 2 teachers
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Work Period with Ashley With: Dylan',datamembers)
        
        exp_res = {'teacher':'DYLAN',
                   'subject':'None',
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_noteacher(self):
        # work period and nothing else
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        
        _enrich('Work Period',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'None',
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_backslash(self):
        # work period and W/
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Work Period W/ Rahul',datamembers)
        
        exp_res = {'teacher':'RAHUL',
                   'subject':'None',
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_edu_nonworkperiod_nowith(self):
        # work period and just teacher name
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Work Period Alexa',datamembers)
        
        exp_res = {'teacher':'ALEXA',
                   'subject':'None',
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)

    def test_edu_nonworkperiod_noteacher2(self):
        # work period captial W small p nothing else
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Work period',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'None',
                   'lessontype':'nwp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_no_match(self):
        # work period and just teacher name
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        
        with self.assertRaises(Exception):
            _enrich('Foobar',datamembers)
            
    def test_no_match_ex2(self):
        # work period and just teacher name
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        
        with self.assertRaises(Exception):
            _enrich('SS With: Rahul',datamembers)
            
            
    def test_no_match_ex3(self):
        # work period and just teacher name
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        
        with self.assertRaises(Exception):
            _enrich('SS Work Period',datamembers)
            
class Test_SchoolSched_misc(unittest.TestCase):
    
    def test_misc_1(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Lunch Computer Time',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'LUNCH COMPUTER TIME',
                   'lessontype':'break',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
    def test_misc_2(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Reading Period With: Nathaniel',datamembers)
        
        exp_res = {'teacher':'NATHANIEL',
                   'subject':'READING PERIOD',
                   'lessontype':'other',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)        
 
    def test_misc_3(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Animal Research Work Period with:Isaac',datamembers)
        
        exp_res = {'teacher':'ISAAC',
                   'subject':'ANIMAL RESEARCH',
                   'lessontype':'wp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers) 
        
    def test_misc_4(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
 
        with self.assertRaises(Exception):      
            _enrich('SS Work Period With: Ricky',datamembers)   
            
    def test_misc_single_token_teacher(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Melissa',datamembers)
        
        exp_res = {'teacher':'MELISSA',
                   'subject':'None',
                   'lessontype':'psych',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers) 
        
    def test_misc_single_token_subject(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Math',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'MATH',
                   'lessontype':'edu',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers) 
        
    def test_misc5(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Reading Period With: Nathaniel',datamembers)
        
        exp_res = {'teacher':'NATHANIEL',
                   'subject':'READING PERIOD',
                   'lessontype':'other',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)
        
        
    def test_misc6(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Lunch Computer Time',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'LUNCH COMPUTER TIME',
                   'lessontype':'break',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)    
        
    def test_misc7(self):
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],
                          [1,3,4,0])
        
        datamembers = _initdatamembers('lesson',
                                       **_dm)
        
        _enrich('Social Studies Work Period',datamembers)
        
        exp_res = {'teacher':'None',
                   'subject':'SOCIAL STUDIES',
                   'lessontype':'wp',
                   'period':'11:13-11:45',
                   'dow':'Thursday',
                   'userdefid':'1.3.4',
                   'objtype':'lesson',
                   'student':'NATHANIEL'}  

        self.assertEquals(exp_res,datamembers)            
        
        
        
        
       
class Test_SchoolSched_lesson_create(unittest.TestCase):
    
    # test that a lesson object is created properly by asserting
    # the existence and values of each of its attributes

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_(self):
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],[1,0,1,0])
        
        datamembers = _initdatamembers('lesson',**_dm)
        
        _enrich('QUAD CAFE',datamembers)
        
        exp_res=[('objtype','lesson'),
                 ('dow','Monday'),
                 ('teacher','None'),
                 ('subject','QUAD CAFE'),
                 ('lessontype','break'),
                 ('period','9:11-9:51'),
                 ('userdefid','1.0.1'),
                 ('student','NATHANIEL')]
        
        exp_res.sort()
        
        lesson = _lesson_create(datamembers,self.database,self.of)
        
        attr = lesson.attr_get_keyval(include_callable=False,
                                          include_nondataattr=False)
            
        attr.sort()
        
        self.assertEquals(attr,exp_res)
        
class Test_SchoolSched_create_secondary_objects_no_teacher(unittest.TestCase):
    
    # test that when a lesson object is created, all other records
    # that are new are created by asserting the contents of the
    # objfactory store

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_(self):
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],[1,0,1,0])
    
        datamembers = _initdatamembers('lesson',**_dm)
    
        _enrich('QUAD CAFE',datamembers)

        #exp_res = [('None','teacher'),
                   
        exp_res =  [('9:11-9:51','period'),
                   ('NATHANIEL','student'),
                   ('Monday','dow'),
                   ('1.0.1','lesson'),
                   ('break','lessontype'),
                   ('QUAD CAFE','subject')]


        _lesson_create(datamembers,self.database,self.of)

        attr_list = [(obj.userdefid, obj.objtype) for obj in self.of.object_iter() if obj.objtype not in ['objtype','userdefid']]

        attr_list.sort()
        exp_res.sort()
        
        #_pprint(exp_res,attr_list)
        self.assertListEqual(attr_list,exp_res)
        
class Test_SchoolSched_create_secondary_objects_with_teacher(unittest.TestCase):
    
    # test that when a lesson object is created, all other records
    # that are new are created by asserting the contents of the
    # objfactory store

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_(self):
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],[1,0,1,0])
    
        datamembers = _initdatamembers('lesson',**_dm)
    
        _enrich('Science WP With: Kayla',datamembers)

        #exp_res = [('None','teacher'),
                   
        exp_res =  [('KAYLA','teacher'),
                    ('9:11-9:51','period'),
                   ('NATHANIEL','student'),
                   ('Monday','dow'),
                   ('1.0.1','lesson'),
                   ('wp','lessontype'),
                   ('SCIENCE','subject')]


        _lesson_create(datamembers,self.database,self.of)

        attr_list = [(obj.userdefid, obj.objtype) for obj in self.of.object_iter() if obj.objtype not in ['objtype','userdefid']]

        attr_list.sort()
        exp_res.sort()
        
        #_pprint(exp_res,attr_list)
        self.assertListEqual(attr_list,exp_res)
    
        
class Test_SchoolSched_create_secondary_objects_type(unittest.TestCase):
    
    # test that when a lesson object is created, all other records
    # that are new are created by asserting that the values are of
    # the correct object type

    def setUp(self):
        self.database = Database('htmlparser',True)
        self.of = ObjFactory(True)
    
    def test_(self):
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],[1,0,1,0])
    
        datamembers = _initdatamembers('lesson',**_dm)
    
        _enrich('QUAD CAFE',datamembers)
        
        _lesson_create(datamembers,self.database,self.of)

        attr_list = [(obj, obj.objtype) for obj in self.of.object_iter()]

        for obj in self.of.object_iter():
            self.assertTrue(isinstance(obj,eval(obj.objtype)))
            
        with self.database:
            pass

class Test_SchoolSched_persist(unittest.TestCase):

    # test that a lesson object is persisted to the db correctly
    # by asserting the fields written into the database table
    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
    
    def test_persist_lesson(self):
        
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],[1,2,2,0])
    
        datamembers = _initdatamembers('lesson',**_dm)
    
        _enrich('QUAD CAFE',datamembers)
        
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
        
class Test_SchoolSched_persist_multi(unittest.TestCase):

    # test that a lesson object is persisted to the db correctly
    # by asserting the fields written into the database table
    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
        
        self._create('Math WP With: Moira', [1,2,7,0])
        self._create('HUMANITIES',[1,4,9,0])
        self._create('Math WP With: Moira',[1,2,3,0])
        self._persist()

    def _create(self,lessonname,params):
        
        _dm = _cdict(['schedule_num','day_num','period_num','student_num'],params)
        datamembers = _initdatamembers('lesson',**_dm)
        _enrich(lessonname,datamembers)
        
        _lesson_create(datamembers,self.database,self.of)

    def _persist(self):
        
        with self.database:
            for obj in self.of.object_iter():
                obj.persist()
            
    def test_persist_multi_lesson(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'lesson'),3)
            
    def test_persist_multi_teacher(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'teacher'),1)
            _,rowvals = tbl_rows_get(self.database,'teacher',['userdefid'])
                 
        self.assertListEqual(rowvals,[['MOIRA']])
            
    def test_persist_multi_subject(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'subject'),2)
            _,rowvals = tbl_rows_get(self.database,'subject',['userdefid'])
        
        rowvals.sort()         
        self.assertListEqual(rowvals,[['HUMANITIES'],['MATH']])
            
    def test_persist_multi_dow(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'dow'),2)
            _,rowvals = tbl_rows_get(self.database,'dow',['userdefid'])
        
        rowvals.sort()   
        self.assertListEqual(rowvals,[['Friday'],['Wednesday']])
        
    def test_persist_multi_period(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'period'),3)
            _,rowvals = tbl_rows_get(self.database,'period',['userdefid'])
        
        rowvals.sort()
        self.assertListEqual(rowvals,[['10:33-11:13'],['1:07-1:47'],['2:30-3:00']])
            
    def test_persist_multi_student(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'student'),1)
            _,rowvals = tbl_rows_get(self.database,'student',['userdefid'])
                 
        self.assertListEqual(rowvals,[['NATHANIEL']])
    
    
class Test_SchoolSched_schdule_load_1lesson(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
        
        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f,num_periods=1,num_students=1,num_days=1)

        schedule_load(self.schedule, self.of, self.database)
        
    def test_schdload_lesson(self):
        schedule_load(self.schedule, self.of, self.database)
        
        exp_res = ['0.0.0']
        exp_res.sort()
        
        _res = self.of.query('lesson')
        
        
        _resstr =  [str(_r) for _r in _res]
        _resstr.sort()
        
        self.assertListEqual(exp_res, _resstr)

        
    def test_schdload_subject(self):
        schedule_load(self.schedule, self.of, self.database)
        
        _res = self.of.query('subject')        
        _resstr =  [str(_r) for _r in _res] 
        
        _resstr.sort()
        
        self.assertListEqual(['MOVEMENT'],
                             _resstr)
        
    def test_schdload_objtype(self):
        schedule_load(self.schedule, self.of, self.database)
        
        exp_res = ['period','student','dow','lessontype','subject','lesson']
        exp_res.sort()
        
        _res = self.of.query('objtype')        
        _resstr =  [str(_r) for _r in _res] 
        
        _resstr.sort()
        
        self.assertListEqual(exp_res,_resstr)
        
                
class Test_SchoolSched_schdule_load(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
        
        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f,num_periods=2,num_students=1)

        schedule_load(self.schedule, self.of, self.database)
        
    def test_schdload_lesson(self):
        schedule_load(self.schedule, self.of, self.database)
        
        exp_res = ['0.0.0','0.1.0','0.2.0','0.3.0','0.4.0','0.0.1','0.1.1','0.2.1','0.3.1','0.4.1']
        exp_res.sort()
        
        _res = self.of.query('lesson')
        
        
        _resstr =  [str(_r) for _r in _res]
        _resstr.sort()
        
        self.assertListEqual(exp_res, _resstr)

        
    def test_schdload_subject(self):
        schedule_load(self.schedule, self.of, self.database)
        
        _res = self.of.query('subject')        
        _resstr =  [str(_r) for _r in _res] 
        
        _resstr.sort()
        
        self.assertListEqual(['ART','CHESS','CORE','MOVEMENT','READING PERIOD','SCIENCE','STEM','YOGA'],
                             _resstr)
        
    def test_schdload_teacher(self):
        schedule_load(self.schedule, self.of, self.database)
        
        _res = self.of.query('teacher')        
        _resstr =  [str(_r) for _r in _res] 
        
        _resstr.sort()
        
        self.assertListEqual(['NATHANIEL','RAHUL'],
                             _resstr)
        
    def test_schdload_dow(self):
        schedule_load(self.schedule, self.of, self.database)
        
        _res = self.of.query('dow')        
        _resstr =  [str(_r) for _r in _res] 
        
        _resstr.sort()
        
        self.assertListEqual(['Friday','Monday','Thursday','Tuesday','Wednesday'],
                             _resstr)
        
    def test_schdload_objtype(self):
        schedule_load(self.schedule, self.of, self.database)
        
        exp_res = ['period','student','dow','lessontype','subject','lesson','teacher']
        exp_res.sort()
        
        _res = self.of.query('objtype')        
        _resstr =  [str(_r) for _r in _res] 
        
        _resstr.sort()
        
        self.assertListEqual(exp_res,_resstr)
        
                
class Test_SchoolSched_schdule_load_persist(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
        
        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f,num_periods=2,num_students=1)
        
        schedule_load(self.schedule, self.of, self.database)
        schedule_persist(self.of,self.database)

    def test_schdloadpsist_teacher(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'teacher'),2)
            _,rowvals = tbl_rows_get(self.database,'teacher',['userdefid'])
        
            rowvals.sort()   
            self.assertListEqual(rowvals,[['NATHANIEL'],['RAHUL']])
            
    def test_schdloadpsist_subject(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'subject'),8)
            _,rowvals = tbl_rows_get(self.database,'subject',['userdefid'])
        
            rowvals.sort()   
            self.assertListEqual(rowvals,[['ART'],['CHESS'],['CORE'],['MOVEMENT'],['READING PERIOD'],['SCIENCE'],['STEM'],['YOGA']])

    def test_schdloadpsist_lessons(self):
        self.database = Database('htmlparser',True)
        
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'lesson'),10)

class Test_SchoolSched_schdule_load_persist_1student_1period_all_fields(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
        
        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f,num_students=1,num_periods=1)
        
        schedule_load(self.schedule, self.of, self.database)
        schedule_persist(self.of,self.database)
                         
    def test_schdloadpsist_lessons(self):
        self.database = Database('htmlparser',True)
        exp_results = [['8:30-9:10','Monday','MOVEMENT','None','other'], ['8:30-9:10','Tuesday','MOVEMENT','None','other'],
                       ['8:30-9:10','Wednesday','CHESS','RAHUL','break'],['8:30-9:10','Thursday','CORE','None','other'],
                       ['8:30-9:10','Friday','STEM','None','edu']]

        with self.database:
            self.assertEquals(tbl_count_get(self.database,'lesson'),5)
            _,rowvals = tbl_rows_get(self.database,'lesson',['period','dow','subject',
                                                             'teacher','lessontype'])
            

        self.assertListEqual(rowvals,exp_results)

    def test_schdloadpsistobjtype(self):
        self.database = Database('htmlparser',True)
        exp_results =  ['period','student','teacher','dow','lessontype','subject','lesson']

        with self.database:
            self.assertEquals(tbl_count_get(self.database,'objtype'),7)
            _,rowvals = tbl_rows_get(self.database,'objtype',['userdefid'])
            
        self.assertListEqual(rowvals,exp_results)
        
    def test_schdloadpsiststudent(self):
        self.database = Database('htmlparser',True)
        exp_results =  [['NATHANIEL']]

        with self.database:
            self.assertEquals(tbl_count_get(self.database,'student'),1)
            _,rowvals = tbl_rows_get(self.database,'student',['userdefid'])
            
        self.assertListEqual(rowvals,exp_results)       
        
class Test_SchoolSched_schdule_load_persist_1student(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
        
        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f,num_students=1)
        
        schedule_load(self.schedule, self.of, self.database)
        schedule_persist(self.of,self.database)
                         
    def test_schdloadpsist_lessons(self):
        self.database = Database('htmlparser',True)
        exp_results = [['8:30-9:10','Monday','MOVEMENT','None','other'], 
                       ['8:30-9:10','Tuesday','MOVEMENT','None','other'], 
                       ['8:30-9:10','Wednesday','CHESS','RAHUL','break'], 
                       ['8:30-9:10','Thursday','CORE','None','other'], 
                       ['8:30-9:10','Friday','STEM','None','edu'], 
                       ['9:11-9:51','Monday','YOGA','None','other'], 
                       ['9:11-9:51','Tuesday','ART','None','edu'], 
                       ['9:11-9:51','Wednesday','READING PERIOD','NATHANIEL','other'], 
                       ['9:11-9:51','Thursday','SCIENCE','None','edu'], 
                       ['9:11-9:51','Friday','MOVEMENT','None','other'],
                       ['9:52-10:32','Monday','ELA','None','edu'], 
                       ['9:52-10:32','Tuesday','MATH','None','edu'], 
                       ['9:52-10:32','Wednesday','MUSIC','None','other'], 
                       ['9:52-10:32','Thursday','CHESS','RAHUL','break'], 
                       ['9:52-10:32','Friday','HUMANITIES','None','edu'],
                       ['10:33-11:13','Monday','None','DYLAN','nwp'], 
                       ['10:33-11:13','Tuesday','MATH','MOIRA','wp'], 
                       ['10:33-11:13','Wednesday','MATH','None','edu'],
                       ['10:33-11:13','Thursday','None','DYLAN','nwp'],
                       ['10:33-11:13','Friday','OT','None','edu'], 
                       ['11:13-11:45','Monday','LUNCH COMPUTER TIME','None','break'],
                       ['11:13-11:45','Tuesday','LUNCH COMPUTER TIME','None','break'], 
                       ['11:13-11:45','Wednesday','LUNCH COMPUTER TIME','None','break'], 
                       ['11:13-11:45','Thursday','LUNCH COMPUTER TIME','None','break'],
                       ['11:13-11:45','Friday','LUNCH COMPUTER TIME','None','break'],
                       ['11:45-12:25','Monday','ANIMAL RESEARCH','ISAAC','wp'], 
                       ['11:45-12:25','Tuesday','SOCIAL STUDIES','None','edu'],
                       ['11:45-12:25','Wednesday','MATH','DYLAN','wp'], 
                       ['11:45-12:25','Thursday','None','EMILY','psych'], 
                       ['11:45-12:25','Friday','None','None','None'], 
                       ['12:26-1:06','Monday','YOGA','DYLAN','other'], 
                       ['12:26-1:06','Tuesday','None','DYLAN','nwp'], 
                       ['12:26-1:06','Wednesday','None','RACHEL','nwp'], 
                       ['12:26-1:06','Thursday','SOCIAL STUDIES','None','edu'],
                       ['12:26-1:06','Friday','None','None','None'], 
                       ['1:07-1:47','Monday','SCIENCE','None','edu'], 
                       ['1:07-1:47','Tuesday','SOCIAL STUDIES','DYLAN','wp'],
                       ['1:07-1:47','Wednesday','MOVEMENT','None','other'], 
                       ['1:07-1:47','Thursday','SOCIAL STUDIES','RICKY','wp'],
                       ['1:07-1:47','Friday','None','None','None'],
                       ['1:48-2:28','Monday','SCIENCE','KAYLA','wp'], 
                       ['1:48-2:28','Tuesday','CORE','EMILY','other'], 
                       ['1:48-2:28','Wednesday','ELA','None','edu'],
                       ['1:48-2:28','Thursday','CHESS','RAHUL','break'], 
                       ['1:48-2:28','Friday','None','None','None'], 
                       ['2:30-3:00','Monday','END COMPUTER TIME','None','break'],
                       ['2:30-3:00','Tuesday','END COMPUTER TIME','None','break'], 
                       ['2:30-3:00','Wednesday','END COMPUTER TIME','None','break'],
                       ['2:30-3:00','Thursday','END COMPUTER TIME','None','break'],
                       ['2:30-3:00','Friday','None','None','None']]

        with self.database:
            self.assertEquals(tbl_count_get(self.database,'lesson'),50)
            _,rowvals = tbl_rows_get(self.database,'lesson',['period','dow','subject',
                                                             'teacher','lessontype'])
            
        self.assertListEqual(rowvals,exp_results)

 
                         
class Test_SchoolSched_schdule_load_persist_big_multistudent(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)

        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f,num_periods=2)

        schedule_load(self.schedule, self.of, self.database)
        schedule_persist(self.of,self.database)

    def test_schdloadpsist_lesson(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'lesson'),15*2*5)

    def test_schdloadpsist_student(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'student'),15)
            
    def test_schdloadpsist_days(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'dow'),5)
            
            
class Test_SchoolSched_schdule_load_persist_all(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)

        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f)

        schedule_load(self.schedule, self.of, self.database)
        schedule_persist(self.of,self.database)
        
    def test_lessons(self):
        self.database = Database('htmlparser')
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'lesson'),15*10*5)

            
class Test_SchoolSched_schdule_load_persist_big(unittest.TestCase):

    def setUp(self):
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)

        f = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html" 
        self.schedule = htmlschedule_slice(f,num_students=2)

        schedule_load(self.schedule, self.of, self.database)
        schedule_persist(self.of,self.database)

    def test_schdloadpsist_lesson(self):
        self.database = Database('htmlparser',True)
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'lesson'),100)

    def test_schdloadpsist_teacher(self):
        
        exp_res = ['DYLAN','EMILY','ISAAC','KAYLA','MELISSA','MOIRA','NATHANIEL','RACHEL','RAHUL', \
                   'RICKY']
        
        self.database = Database('htmlparser',True)
        with self.database:
            _,rowvals = tbl_rows_get(self.database,'teacher',['userdefid'])
        
            rowvals.sort()   
            
            exp_res.sort()
            _exp_res = [[unicode(e,'utf-8')] for e in exp_res]
            
            self.assertListEqual(rowvals,_exp_res)
            
    def test_schdloadpsist_subject(self):
        self.database = Database('htmlparser',True)
        exp_res = ['Movement','Chess','OT','Lunch Computer Time','End Computer Time', \
                   'Core','Stem','YOGA','Art','Reading Period','Science','ELA', \
                   'Math','Music','Humanities','Animal Research','Social Studies', \
                   'Psychology','Independent Reading','Regents Prep','Regions Prep', \
                   'Italian','Student News'] 
        with self.database:
            self.assertEquals(tbl_count_get(self.database,'subject'),23)    

            _exp_res = [unicode(e.upper(),'utf-8') for e in exp_res]
            
            _exp_res.sort()
            exp_res = [[e] for e in _exp_res]
            
            _,rowvals = tbl_rows_get(self.database,'subject',['userdefid'])
            
            rowvals.sort()

            self.assertListEqual(rowvals,exp_res)

class Test_SchoolSched_token_type_get(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_teacher(self):
        self.assertEqual(_token_type_get('MELISSA'),'teacher')
        
    def test_subject(self):
        self.assertEqual(_token_type_get('LUNCH COMPUTER TIME'),'break')
        

class Test_SchoolSched_validate_token(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_teacher(self):
        self.assertTrue(_validate_token('MELISSA'))
        
    def test_subject(self):
        self.assertTrue(_validate_token('LUNCH COMPUTER TIME'))
        
    def test_valudate_false(self):
        with self.assertRaises(Exception):
            _validate_token('LUNCHY COMPUTER TIME')

    def test_validate_psych(self):
        self.assertTrue(_validate_token('COUNSELING'))

    def test_validate_teacher(self):
        self.assertTrue(_validate_token('ASHLEY'))
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_enrich))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_misc))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_lesson_create))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_create_secondary_objects_with_teacher))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_create_secondary_objects_no_teacher))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_create_secondary_objects_type))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_persist))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_persist_multi))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_1lesson))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_persist))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_persist_1student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_persist_1student_1period_all_fields))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_persist_1student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_persist_big))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_token_type_get))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_validate_token))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_persist_big_multistudent))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_schdule_load_persist_all))
     
    
    unittest.TextTestRunner(verbosity=2).run(suite)