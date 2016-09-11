import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")

from Tkinter import *
from ttk import *

import unittest

from sswizard import schoolschedgeneric, WizardUI, teachers
from database_util import Database
from misc_utils_objectfactory import ObjFactory
from misc_utils import Log

class Test_Load_From_Database(unittest.TestCase):

    def setUp(self):
        self.master = Tk()
        
        self.database = Database('test')
        self.of = ObjFactory(True)
        self.ui = WizardUI(self.master, self.database, self.of)
        
    def test_from_db_to_grid(self):
        
        expected_results =[['Stan', 'Galina', 'Samantha', 'Amelia', 'Paraic'],
                           ['8:30-9:10', 'NATHANIEL', 'ORIG', 'TRISTAN', 'COBY', 'YOSEF'],
                           ['9:11-9:51', 'LUCY', 'DONOVAN', 'BOOKER', 'ASHER', 'JAKE']]
        self.ui.load(0)
        
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)
        
    def test_create_all_object_types_after_save(self):
        # test just that of has created an index for each type of object expected #
        expected_results = ['lesson','schedule','dow','subject','lessontype','objtype',
                            'userobjid','period','student','saveversion','teacher']
        
        expected_results.sort()
        
        self.ui.load_save(0)
        
        results = self.of.query()
        results.sort()
        
        self.master.mainloop()
        
        self.assertListEqual(results, expected_results)
        
    def test_student_object_after_save(self):
        # test that objects of type student are being created
        
        self.ui.load_save(0)
        
        results = self.of.query('student')
        
        for obj in results:
            self.assertEqual(obj.__class__.__name__,'student')
            
    def test_student_object_attr_after_save(self):
        # test that the objects created have the correct member attr and attrvals
        
        self.ui.load_save(0)
        
        results = self.of.query('student')
        
        student_obj = results[0]
        name = getattr(student_obj,'name')
        
        self.assertEquals(name,getattr(student_obj,'objid'))
        self.assertEquals(name,getattr(student_obj,'userobjid'))
        self.assertEquals('student',getattr(student_obj,'objtype'))
        
        self.assertEqual('ObjFactory', getattr(student_obj,'of').__class__.__name__)
        self.assertEqual('Log', getattr(student_obj,'log').__class__.__name__)\
            
    def test_lesson_object_attr_after_save(self):
        # test that the objects created have the correct member attr and attrvals
        
        self.ui.load_save(0)
        
        results = self.of.query('lesson')
        
        lesson_obj = results[0]
        objid = getattr(lesson_obj,'objid')

        self.assertEquals(objid,getattr(lesson_obj,'userobjid'))
        self.assertEquals('lesson',getattr(lesson_obj,'objtype'))
        self.assertEquals('Tuesday',getattr(lesson_obj,'dow'))
        self.assertEquals('MATH',getattr(lesson_obj,'subject'))
        self.assertEquals('wp',getattr(lesson_obj,'lessontype'))
        self.assertIn(getattr(lesson_obj,'teacher'),teachers)
        self.assertEqual('ObjFactory', getattr(lesson_obj,'of').__class__.__name__)
        self.assertEqual('Log', getattr(lesson_obj,'log').__class__.__name__)
        
                                  
    def tearDown(self):
        pass
        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_From_Database))

    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


