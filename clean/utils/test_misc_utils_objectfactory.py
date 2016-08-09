
import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils_objectfactory import GenericBase, ObjFactory
from database_table_util import dbtblgeneric
from database_util import Database

import unittest

class Foobar(GenericBase):
    def __init__(self,objid,**kwargs):

        super(Foobar,self).__init__(**kwargs)
      
class Test_ObjFrameworkBasic(unittest.TestCase):

    def setUp(self):
        foobar= ObjFactory(__logger__=True).new('Foobar',
                                                objid='0.0.0',
                                                modname=__name__,
                                                student = 'booker',
                                                period=2,
                                                dow=3)
        

        
    def test_num_obj_created(self):
        self.assertEquals(len(ObjFactory().store['Foobar']),1)
        
    def test_correct_keys_created(self):
        self.assertTrue(ObjFactory().store['Foobar'].has_key('0.0.0'))
    
    def test_objects_created_stored(self):
        _lesson = ObjFactory().store['Foobar']['0.0.0']
        self.assertTrue(isinstance(_lesson,Foobar))

    def test_objects_have_attributes(self):
        _lesson = ObjFactory().store['Foobar']['0.0.0']        
        self.assertEquals(_lesson.student,'booker')
        self.assertEquals(_lesson.period,2)
        self.assertEquals(_lesson.dow,3)

class DBFoobar(dbtblgeneric):
    pass
      
class Test_ObjFramework_Database(unittest.TestCase):


    def setUp(self):
        self.database = Database('foobar')
        self.foobar= ObjFactory().new('DBFoobar',
                                 objid='0.0.0',
                                 constructor='datamembers',
                                 modname=__name__,
                                 database=self.database,
                                 datamembers={'student':'booker',
                                              'period':2,
                                              'dow':3})

    def test_num_obj_created(self):
        self.assertEquals(len(ObjFactory().store['DBFoobar']),1)
        
    def test_correct_keys_created(self):
        self.assertTrue(ObjFactory().store['DBFoobar'].has_key('0.0.0'))
    
    def test_objects_created_stored(self):
        _lesson = ObjFactory().store['DBFoobar']['0.0.0']
        self.assertTrue(isinstance(_lesson,DBFoobar))

    def test_objects_have_attributes(self):
        _lesson = ObjFactory().store['DBFoobar']['0.0.0']        
        self.assertEquals(_lesson._dm_student,'booker')
        self.assertEquals(_lesson._dm_period,2)
        self.assertEquals(_lesson._dm_dow,3)
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkBasic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database))
    unittest.TextTestRunner(verbosity=2).run(suite) 