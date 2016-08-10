import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils_generic import GenericBase
from misc_utils_enum import enum
from misc_utils_objectfactory import ObjFactory
from database_table_util import dbtblgeneric
from database_util import Database, tbl_create
import unittest

period_enum = ['8:30-9:10','9:11-9:51','9:52-10:32','10:33-11:13',
               '11:13-11:45','11:45-12:25','12:26-1:06','1:07-1:47',
               '1:48-2:28','2:30-3:00']

day_enum = ['Monday','Tuesday','Wednesday','Thursday','Friday']


class Lesson(dbtblgeneric):
    def __init__(self,objid,**kwargs):
        
        super(Lesson,self).__init__(**kwargs)
        self.objid = objid

    def __repr__(self):
        return(self.objid)

    def attr_set(self,of,database,name,clsname):
        self.teacher = of.new(clsname,
                              objid=name,
                              constructor='datamembers',
                              database=database,
                              modname=__name__,
                              dm={'name':name})    
        
class Teacher(dbtblgeneric):
    def __repr__(self):
        return(self.objid)

class Test_HTMLParserBasic(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar',True)

        lesson=self.of.new('Lesson',
                           objid='lesson0',
                           constructor='datamembers',
                           database=self.database,
                           modname=__name__,
                           dm={'student':'booker',
                               'period':2,
                               'dow':3})

        lesson.attr_set(self.of,self.database,'fran','Teacher')
        lesson.type="psych"
        
    def test_num_obj_created_lesson(self):
        
        self.assertEquals(len(self.of.query('Lesson')),1)
        
    def test_num_obj_created_teacher(self):
        
        self.assertEquals(len(self.of.query('Teacher')),1)
        
    def test_correct_keys_created_lesson(self):
        self.assertTrue(self.of.object_exists('Lesson','lesson0'))
        
    def test_correct_keys_created_teacher(self):
        self.assertTrue(self.of.object_exists('Teacher','fran'))
    
    def test_objects_created_stored_lesson(self):
        _lesson = self.of.object_get('Lesson','lesson0')
        self.assertTrue(isinstance(_lesson,Lesson))
      
    def test_objects_created_stored_teacher(self):
        _teacher = self.of.object_get('Teacher','fran')
        self.assertTrue(isinstance(_teacher,Teacher))
        
    def test_object_joins(self):
        _teacher = self.of.object_get('Lesson','lesson0').teacher
        self.assertTrue(isinstance(_teacher,Teacher))
        self.assertEquals(_teacher.name,'fran')
        
    def test_objects_have_attributes(self):
        _lesson = self.of.object_get('Lesson','lesson0')
     
        self.assertEquals(_lesson.student,'booker')
        self.assertEquals(_lesson.period,2)
        self.assertEquals(_lesson.dow,3)
        
class Test_HTMLParserPersist(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')

        lesson=self.of.new('Lesson',
                           objid='lesson0',
                           constructor='datamembers',
                           database=self.database,
                           modname=__name__,
                           dm={'student':'\"booker\"',
                               'period':2,
                               'dow':3})

        lesson.attr_set(self.of,self.database,'\"fran\"','Teacher')
        lesson.type="psych"
        
    def test_persist(self):
        
        with self.database:
            for obj in self.of.object_iter():
                obj.persist()
            
        with self.database:
            self.assertEquals([['booker']],self.database.execute("select student from Lesson"))
            self.assertEquals([['fran']],self.database.execute("select name from Teacher"))
            
        self.database = Database('foobar',True)
        with self.database:
            pass
        
class Test_HTMLParserPersistScale(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        with self.database:
            tbl_create(self.database,'Lesson',[('student','text'),
                                               ('period','integer'),
                                               ('dow','integer'),
                                               ('__timestamp','text'),
                                               ('__id','text')])
            
            tbl_create(self.database,'Teacher',[('name','text'),
                                               ('__timestamp','text'),
                                               ('__id','text')])

         
        
        self.teachers = ['fran','dave','brian','steve','paul','damian','roger','jon','graeme','ringo']
        for day in range(5):
            for period in range(10):
                lesson=self.of.new('Lesson',
                                   objid='lesson'+str(day)+str(period),
                                   constructor='datamembers',
                                   database=self.database,
                                   modname=__name__,
                                   dm={'student':'\"booker\"',
                                       'period':period,
                                       'dow':day})

                lesson.attr_set(self.of,self.database,'\"'+self.teachers[period]+'\"','Teacher')
                lesson.type="psych"
                
                
    def test(self):
        with self.database:
            for obj in self.of.object_iter():
                obj.persist(False)
            
        with self.database:
            self.assertEquals(self.database.execute("select count(*) from Lesson",True),50)
            self.assertEquals(self.database.execute("select count(*) from Teacher",True),10)  

        self.database = Database('foobar',True)
        with self.database:
            pass
    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_HTMLParserBasic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_HTMLParserPersist))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_HTMLParserPersistScale))
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)