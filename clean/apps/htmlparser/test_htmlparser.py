import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils_generic import GenericBase
from misc_utils_enum import enum
from misc_utils_objectfactory import ObjFactory
from database_table_util import dbtblgeneric
from database_util import Database
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

class Test_ObjFrameworkBasic(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
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
    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)