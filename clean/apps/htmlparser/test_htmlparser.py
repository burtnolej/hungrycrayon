import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import generic, enum, Log
from misc_utils_objectfactory import ObjFactory
import unittest

period_enum = ['8:30-9:10','9:11-9:51','9:52-10:32','10:33-11:13',
               '11:13-11:45','11:45-12:25','12:26-1:06','1:07-1:47',
               '1:48-2:28','2:30-3:00']

day_enum = ['Monday','Tuesday','Wednesday','Thursday','Friday']


class Lesson(generic):
    def __init__(self,objid,**kwargs):

        super(Lesson,self).__init__(**kwargs)
        self.objid = objid

        if not hasattr(self,'subject'):
            setattr(self,'subject',None)

        if not hasattr(self,'teacher'):
            setattr(self,'teacher',None)

        if not hasattr(self,'type'):
            setattr(self,'type',None)

    def __repr__(self):
        return(self.objid)

    def attr_set(self,name,clsname):
        self.teacher = ObjFactory(__logger__=True).new(clsname,name,
                                        modname=__name__)    
        
class Teacher(generic):
    def __init__(self,name):
        super(Teacher,self).__init__()
        self.name = name

    def __repr__(self):
        return(self.name)

class Test_ObjFrameworkBasic(unittest.TestCase):


    def setUp(self):
        lesson= ObjFactory(__logger__=True).new('Lesson',
                                                '0.0.0',
                                                modname=__name__,
                                                student = 'booker',
                                                period=2,
                                                dow=3)
    
        lesson.attr_set('fran','Teacher')
        lesson.type="psych"
        
    def test_num_obj_created(self):
        self.assertEquals(len(ObjFactory().store['Lesson']),1)
        self.assertEquals(len(ObjFactory().store['Teacher']),1)
        
    def test_correct_keys_created(self):
        self.assertTrue(ObjFactory().store['Lesson'].has_key('0.0.0'))
        self.assertTrue(ObjFactory().store['Teacher'].has_key('fran'))
    
    def test_objects_created_stored(self):
        _lesson = ObjFactory().store['Lesson']['0.0.0']
        self.assertTrue(isinstance(_lesson,Lesson))
        
        _teacher = ObjFactory().store['Teacher']['fran']
        self.assertTrue(isinstance(_teacher,Teacher))
        
    def test_object_joins(self):
        _teacher = ObjFactory().store['Lesson']['0.0.0'].teacher
        self.assertTrue(isinstance(_teacher,Teacher))
        self.assertEquals(_teacher.name,'fran')
        
    def test_objects_have_attributes(self):
        _lesson = ObjFactory().store['Lesson']['0.0.0']        
        self.assertEquals(_lesson.student,'booker')
        self.assertEquals(_lesson.period,2)
        self.assertEquals(_lesson.dow,3)
    
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkBasic)
    unittest.TextTestRunner(verbosity=2).run(suite) 