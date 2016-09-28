
import sys
import os
from os import path as ospath
from misc_utils_objectfactory import GenericBase, ObjFactory
from database_table_util import dbtblgeneric, dbtblfactory
from database_util import Database

import unittest
      
class Test_ObjFrameworkBasic(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory()

        foobar= self.of.new(GenericBase,
                            "Student",
                            objid='booker',
                            modname=__name__,
                            name='booker',
                            age=23)      

    def tearDown(self):
        self.of.reset()
        
    def test_num_obj_created(self):
        self.assertEquals(len(ObjFactory().store['Student']),1)
        
    def test_correct_keys_created(self):
        self.assertTrue(ObjFactory().store['Student'].has_key('booker'))
    
    def test_objects_created_stored(self):
        _student = ObjFactory().store['Student']['booker']
        self.assertEquals(_student.__class__.__name__,"Student")

    def test_objects_have_attributes(self):
        _student = ObjFactory().store['Student']['booker']        
        self.assertEquals(_student.name,'booker')
        self.assertEquals(_student.age,23)
        
class Test_ObjFramework_2_records_same_cls(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory()
        self.obj1= self.of.new(GenericBase,
                               'Student',
                               objid='booker',
                               modname=__name__,
                               name='booker',
                               age=23)
        
        self.obj2= self.of.new(GenericBase,
                               'Student',
                               objid='frank',
                               modname=__name__,
                               name='frank',
                               age=19)
        

    def tearDown(self):
        self.of.reset()
        
    def test_2records_same_class(self):
        names = [obj.name for obj in self.of.query('Student')]
        names.sort()
        self.assertEquals(names,['booker','frank'])
        
class Test_ObjFramework_2_class(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory()
        self.obj1= self.of.new(GenericBase,
                               'Student',
                               objid='booker',
                               modname=__name__,
                               name='booker',
                               age=23)
        
        self.obj2= self.of.new(GenericBase,
                               'Subject',
                               objid='science',
                               modname=__name__,
                               name='science',
                               teacher_name='fran')
        

    def tearDown(self):
        self.of.reset()
        
    def test_2_class(self):
        self.assertListEqual(self.of.query(),['Student','Subject'])
        
class Test_ObjFrameworkDupeID(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory()
        self.obj1= self.of.new(GenericBase,
                               'Student',
                               objid='booker',
                               modname=__name__)
        
        self.obj2= self.of.new(GenericBase,
                               'Student',
                               objid='booker',
                               modname=__name__)
        

    def tearDown(self):
        self.of.reset()
        
    def test_num_dupe_objid(self):
        self.assertEqual(self.obj1,self.obj2)
        
class Test_ObjFrameworkIter(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory(True)
        self.of.new(GenericBase,
                    'Student',
                    objid='booker',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Student',
                    objid='fred',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Classroom',
                    objid='1a',
                    modname=__name__)
        

    def tearDown(self):
        self.of.reset()
        
    def test_iter(self):
        result = [obj.objid for obj in self.of.object_iter()]
        result.sort()
        
        self.assertListEqual(result,['1a','booker','fred'])
        
#class DBLesson(dbtblgeneric):
#    pass
      
class Test_ObjFramework_Database(unittest.TestCase):


    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        self.foobar= self.of.new(dbtblgeneric,
                                 'DBLesson',
                                 objid='dblesson0',
                                 constructor='datamembers',
                                 modname=__name__,
                                 database=self.database,
                                 dm={'student':'booker',
                                     'period':2,
                                     'dow':3})
        
    def tearDown(self):
        self.of.reset()

    def test_num_obj_created(self):
        self.assertEquals(len(self.of.query('DBLesson')),1)
        
    def test_correct_keys_created(self):
        self.assertTrue(self.of.object_exists('DBLesson','dblesson0'))

    
    def test_objects_created_stored(self):
        _lesson = self.of.object_get('DBLesson','dblesson0')
        self.assertEquals(_lesson.__class__.__name__,"DBLesson")

    def test_objects_have_attributes(self):
        _lesson = self.of.object_get('DBLesson','dblesson0')  
        self.assertEquals(_lesson.student,'booker')
        self.assertEquals(_lesson.period,2)
        self.assertEquals(_lesson.dow,3)
        
class Test_ObjFramework_Database_Derived(unittest.TestCase):
    # pass in a subclass of dbtblgeneric as a baseclass; testing a bug found
    # in schoolschedulewizard
    
    class Dummy(dbtblgeneric):
        pass
    
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        self.foobar= self.of.new(self.Dummy,
                                 'DBLesson',
                                 objid='dblesson0',
                                 constructor='datamembers',
                                 modname=__name__,
                                 database=self.database,
                                 dm={'student':'booker',
                                     'period':2,
                                     'dow':3})
        
    def test_num_obj_created(self):
        self.assertEquals(len(self.of.query('DBLesson')),1)
            
     
class schoolschedgeneric(dbtblgeneric):

    def __init__(self,of,database,recursion=True,**kwargs):
        self.recursion = recursion
        super(schoolschedgeneric,self).__init__(database=database,
                                                **kwargs)
        
        self.of = of
        self.database = database
        
        for k,v in kwargs['dm'].iteritems():
            if v <> 'None':
                if recursion == True:
                    # create objects for all member attributes
                    self.attr_set(v,k)
                                   
    def attr_set(self,name,clsname):        
        datamembers = dict(objtype=clsname,
                           userobjid=name,
                           name=name)
        
        setattr(self,clsname,self.of.new(schoolschedgeneric,
                                         clsname,
                                         objid=name, # unique key to store obj in of
                                         constructor='datamembers',
                                         database=self.database,
                                         of=self.of,
                                         modname=__name__,
                                         recursion=False,
                                         dm=datamembers))

        return(getattr(self,clsname))
        
class Test_ObjFramework_Database_Derived_Nested(unittest.TestCase):
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        datamembers = dict(period='830',
                           student='Booker',
                           teacher='Amelia',
                           saveversion=0,
                           session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,
                                 'DBLesson',
                                 objid='dblesson0',
                                 constructor='datamembers',
                                 database=self.database,
                                 of=self.of,
                                 modname=__name__,
                                 dm=datamembers)
        
    def test_student_objid(self):
        
        obj = self.of.store['student']['Booker']
        
        attr = obj.attr_get_keyval(include_callable=False, 
                                    include_baseattr=True,
                                    include_nondataattr=True)
    
        d = dict(attr)
        self.assertTrue(d.has_key('objid'))
        self.assertEqual(d['objid'],'Booker')

    def test_student_name(self):
        
        obj = self.of.store['student']['Booker']
        
        attr = obj.attr_get_keyval(include_callable=False, 
                                    include_baseattr=True,
                                    include_nondataattr=True)
    
        d = dict(attr)
        self.assertTrue(d.has_key('name'))
        self.assertEqual(d['name'],'Booker')
        
        
class Test_ObjFramework_Database_Derived_Nested_DupeKey(unittest.TestCase):
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        self.datamembers = dict(period='830',
                           student='Booker',
                           teacher='Amelia',
                           saveversion=0,
                           session='AM.AC.SC')


        
        
    def test_student_objid(self):
        
        obj1 = self.of.new(schoolschedgeneric,
                                 'DBLesson',
                                 objid='dblesson0',
                                 constructor='datamembers',
                                 database=self.database,
                                 of=self.of,
                                 modname=__name__,
                                 dm=self.datamembers)
        
        obj2 = self.of.new(schoolschedgeneric,
                                 'DBLesson',
                                 objid='dblesson0',
                                 constructor='datamembers',
                                 database=self.database,
                                 of=self.of,
                                 modname=__name__,
                                 dm=self.datamembers)
        
        print self.of.store['student']
        print obj1.student,obj2.student
        

        

        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkBasic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDupeID))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_2_records_same_cls))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_2_class))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkIter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database_Derived))'''
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database_Derived_Nested))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database_Derived_Nested_DupeKey))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
