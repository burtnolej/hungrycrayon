
import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils_objectfactory import generic, ObjFactory

import unittest

class Foobar(generic):
    def __init__(self,objid,**kwargs):

        super(Foobar,self).__init__(**kwargs)
      
class Test_ObjFrameworkBasic(unittest.TestCase):


    def setUp(self):
        foobar= ObjFactory(__logger__=True).new('Foobar',
                                                '0.0.0',
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
         
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkBasic)
    unittest.TextTestRunner(verbosity=2).run(suite) 