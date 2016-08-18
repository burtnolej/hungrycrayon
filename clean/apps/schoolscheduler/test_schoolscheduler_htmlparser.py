import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
import unittest
from database_util import Database, tbl_count_get
from misc_utils_objectfactory import ObjFactory
from schoolscheduler_htmlparser import htmlschedule_parse, htmlschedule_slice
from schoolscheduler import  schedule_load

class Test_SchoolSched_htmlparser(unittest.TestCase):

    def setUp(self):
        filename = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html"
        self.schedule = htmlschedule_parse(filename)
        self.exp_students_num = 15
        self.exp_periods_num = 10
        self.exp_day_num = 5
        self.exp_lessons_num = self.exp_periods_num * self.exp_students_num * self.exp_day_num
        
    def test_num_students(self):
        # student and schedule are 1 to 1
        self.assertEquals(len(self.schedule),self.exp_students_num)
        #import pprint
        #print pprint.pprint(schedule)
        
    def test_num_periods(self):
        # assume all periods are the same length
        self.assertEquals(len(self.schedule[0])-1,self.exp_periods_num)
        
    def test_num_days(self):
        # assume all days are the same length
        self.assertEquals(len(self.schedule[0][0])-2,self.exp_day_num)
        
    def test_num_lessons(self):
        num_lessons=0
        for schedule_num in range(len(self.schedule)):
            for period_num in range(1,self.exp_periods_num+1):
                num_lessons += self.exp_day_num
                
        self.assertEquals(num_lessons,self.exp_lessons_num)
     
class Test_SchoolSched_htmlschedule_slice_1period_1_student(unittest.TestCase):
    
    def setUp(self):
        filename = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html"
        self.exp_students_num = 1
        self.exp_periods_num = 1
        self.exp_day_num = 5
        self.schedule = htmlschedule_slice(filename,
                                           num_days=self.exp_day_num,
                                           num_periods=self.exp_periods_num,
                                           num_students=self.exp_students_num)
        self.exp_lessons_num = self.exp_periods_num * self.exp_day_num * self.exp_students_num
    
    def test_num_students(self):
        # student and schedule are 1 to 1
        self.assertEquals(len(self.schedule),self.exp_students_num)
        
    def test_num_periods(self):
        # assume all periods are the same length
        self.assertEquals(len(self.schedule[0]),self.exp_periods_num)
        
    def test_num_days(self):
        # assume all days are the same length

        self.assertEquals(len(self.schedule[0][0]),self.exp_day_num)
        
    def test_num_lessons(self):
        num_lessons=0
        for schedule_num in range(len(self.schedule)):
            for period_num in range(1,self.exp_periods_num+1):
                num_lessons += self.exp_day_num
                
        self.assertEquals(num_lessons,self.exp_lessons_num)
        
    def test_content(self):
        
        exp_res = [[['Movement', 'Movement', 'Chess With: Rahul', 'Core', 'Stem']]]
        self.assertListEqual(self.schedule,exp_res)

class Test_SchoolSched_htmlschedule_slice(unittest.TestCase):
    
    def setUp(self):
        filename = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html"
        self.exp_students_num = 15
        self.exp_periods_num = 2
        self.exp_day_num = 5
        self.schedule = htmlschedule_slice(filename,self.exp_day_num,self.exp_periods_num)
        self.exp_lessons_num = self.exp_periods_num * self.exp_students_num * self.exp_day_num
    
    def test_num_students(self):
        # student and schedule are 1 to 1
        self.assertEquals(len(self.schedule),self.exp_students_num)
        #import pprint
        #print pprint.pprint(schedule)
        
    def test_num_periods(self):
        # assume all periods are the same length
        self.assertEquals(len(self.schedule[0]),self.exp_periods_num)
        
    def test_num_days(self):
        # assume all days are the same length
        #self.assertEquals(len(self.schedule[0][0])-2,self.exp_day_num)
        self.assertEquals(len(self.schedule[0][0]),self.exp_day_num)
        
    def test_num_lessons(self):
        num_lessons=0
        for schedule_num in range(len(self.schedule)):
            for period_num in range(1,self.exp_periods_num+1):
                num_lessons += self.exp_day_num
                
        self.assertEquals(num_lessons,self.exp_lessons_num)
        

            
class Test_SchoolSched_htmlschedule_slice_all_students_1lesson(unittest.TestCase):
    
    def setUp(self):
        filename = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html"
        self.exp_periods_num = 1
        self.exp_day_num = 1
        self.schedule = htmlschedule_slice(filename,self.exp_day_num,self.exp_periods_num)
        
    def test_content(self):
        
        exp_res = [[['Movement']], [['Movement']], [['Movement']], [['ELA']], 
                     [['Mentoring With: chris']],[['Math']],[['Movement']],
                     [['Movement']],[['Music']],[['Music']],[['Music']],[['Social Studies']],
                     [['Movement']],[['Movement']],[['Movement']]]

        self.assertListEqual(self.schedule,exp_res)

        
class Test_SchoolSched_htmlschedule_slice_2periods_1student_persist(unittest.TestCase):
    
    def setUp(self):
        filename = "/home/burtnolej/Development/pythonapps3/clean/apps/schoolscheduler/schedule.html"
        self.schedule = htmlschedule_slice(filename,
                                           num_periods = 2,
                                           num_students = 1)
        
        self.database = Database('htmlparser')
        self.of = ObjFactory(True)
        
        schedule_load(self.schedule,self.of,self.database)
        
    def test_content_subject(self):
        
        exp_res = ['MOVEMENT', 'CHESS', 'CORE','STEM','YOGA','ART','READING PERIOD','SCIENCE']

        res = [str(res) for res in self.of.query('subject')]
        self.assertListEqual(res,exp_res)
        
    def test_content_teacher(self):
        
        exp_res = ['RAHUL', 'NATHANIEL']
        res = [str(res) for res in self.of.query('teacher')]
        self.assertListEqual(res,exp_res)
        
    def test_content_student(self):
        
        exp_res = ['NATHANIEL']
        res = [str(res) for res in self.of.query('student')]
        self.assertListEqual(res,exp_res)
        
    def test_content_userdefid(self):
        
        exp_res = ['0.0.0','0.1.0','0.2.0','0.3.0','0.4.0',
                   '0.0.1','0.1.1','0.2.1','0.3.1','0.4.1']
        res = [str(res) for res in self.of.query('userdefid')]
        self.assertListEqual(res,exp_res) 
        
    def test_content_lessontype(self):
        
        exp_res = ['other','break','edu']
        res = [str(res) for res in self.of.query('lessontype')]
        self.assertListEqual(res,exp_res)  
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_htmlparser))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_htmlschedule_slice))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_htmlschedule_slice_1period_1_student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_htmlschedule_slice_all_students_1lesson))
    
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_SchoolSched_htmlschedule_slice_2periods_1student_persist))
    
    unittest.TextTestRunner(verbosity=2).run(suite)