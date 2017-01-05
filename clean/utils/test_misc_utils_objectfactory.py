
import sys
import os
from os import path as ospath
from misc_utils_objectfactory import GenericBase, ObjFactory
from database_table_util import dbtblgeneric, dbtblfactory, tbl_rows_get
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
        
        #self.of = of
        self.database = database
        
        for k,v in kwargs['dm'].iteritems():
            if v <> 'None':
                if recursion == True:
                    # create objects for all member attributes
                    self.attr_set(v,k,of)
                                   
    def attr_set(self,name,clsname,of):        
        datamembers = dict(objtype=clsname,
                           userobjid=name,
                           name=name)
        
        setattr(self,clsname,of.new(schoolschedgeneric,
                                         clsname,
                                         objid=name, # unique key to store obj in of
                                         constructor='datamembers',
                                         database=self.database,
                                         of=of,
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
        
        #print self.of.store['student']
        #print obj1.student,obj2.student    
        
        self.assertEqual(str(obj1.student),str(obj2.student))
        
class Test_ObjFramework_Database_Derived_DB(unittest.TestCase):
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
        self.foobar.keepversion = True
        
    def test_persist(self):

        with self.database:
            self.foobar.persist()

        self.database = Database('foobar',True)
        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'DBLesson',['student','teacher']) 
            
            self.assertEquals([['Booker','Amelia']],tbl_rows)
            
    def test_persist_customtimestamp(self):
        
        self.foobar.customtimestamp = "%y%m%d_%H%M%S"
        with self.database:
            self.foobar.persist()

        self.database = Database('foobar',True)
        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'DBLesson',['__timestamp']) 
            
            self.assertTrue(13,len(tbl_rows[0][0]))
            
    def test_update_1field(self):
        
        expected_results = [[u'830', u'AM.AC.SC', u'Booker', u'Amelia', u'version'], 
                            [u'830', u'AM.AC.SC', u'Booker', u'Aaron', u'current']]
        self.foobar.customtimestamp = "%y%m%d_%H%M%S"
        with self.database:
            self.foobar.persist()
            self.foobar.update('teacher',"\"Aaron\"")

        self.database = Database('foobar',True)
        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'DBLesson',['period','session','student','teacher','__version'] ) 
            
            self.assertListEqual(tbl_rows,expected_results)

class Test_ObjFrameworkDumpNested(unittest.TestCase):

    def setUp(self):
        self.of = ObjFactory(True)
        self.obj1 = self.of.new(GenericBase,
                    'Student',
                    objid='booker',
                    nationality='british',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Student',
                    objid='fred',
                    age=23,
                    nationality='british',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Student',
                    objid='fred',
                    age=35,
                    nationality='irish',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Classroom',
                    objid='1a',
                    nationality='swedish',
                    modname=__name__)
        

    def tearDown(self):
        self.of.reset()
        
    '''def test_1clause(self):
        results = self.of.query_advanced('Student',[('objid','booker')])
        
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].objid,'booker')
        
    def test_2clause(self):
        results = self.of.query_advanced('Student',[('nationality','british'),
                                                    ('objid','fred')])
        
        self.assertEquals(len(results),1)
        self.assertEquals(results[0].age,23)'''
        
        
    def test_update_then_search(self):
        ''' make sure that search picks up the updated version of the object '''
        
        self.obj1.nationality = 'indian'
        results = self.of.query_advanced('Student',[('objid','booker')])
        
        self.assertEquals(results[0].nationality,'indian')
        
        
class Test_ObjFrameworkDump(unittest.TestCase):
    
    def setUp(self):
        self.of = ObjFactory(True)
        self.obj1 = self.of.new(GenericBase,
                    'Student',
                    objid='booker',
                    nationality='british',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Student',
                    objid='dave',
                    age=23,
                    nationality='british',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Student',
                    objid='fred',
                    age=35,
                    nationality='irish',
                    modname=__name__)
        
        self.of.new(GenericBase,
                    'Classroom',
                    objid='1a',
                    modname=__name__)
        
    def test_(self):
        results = self.of.dump()
        
        expected_results = [dict(objtype='Student',objid='booker',nationality='british'),
                            dict(objtype='Student',objid='dave',nationality='british',age=23),
                            dict(objtype='Student',objid='fred',nationality='irish',age=35),
                            dict(objtype='Classroom',objid='1a')]
        
        

class Test_ObjFrameworkDump(unittest.TestCase):
    
    def setUp(self):
        self.of = ObjFactory(True)
        self.obj1 = self.of.new(GenericBase,
                    'Student',
                    objid='booker',
                    nationality='british',
                    modname=__name__)
        
    def test_(self):
        from types import StringType,IntType, UnicodeType
        expected_results = [[('pobjid', 'ROOT'),('objid', 'booker'), ('objtype', 'Student'), ('nationality', 'british')]]
                
        _results = self.of.dumpobj()
        results = []
        for result in _results:
            result.pop('id')
            results.append([(k,v) for k,v in result.iteritems() if type(v) in [IntType,StringType,UnicodeType]])
        
        expected_results.sort()
        results.sort()
        
        self.assertListEqual(expected_results,results)
        
class Test_ObjFrameworkDumpNested(unittest.TestCase):
    
    def setUp(self):
        self.of = ObjFactory(True)


        self.student = self.of.new(GenericBase,
                                   'Student',
                                   objid='booker',
                                   nationality='british',
                                   modname=__name__)
        
        self.lesson = self.of.new(GenericBase,
                                  'Lesson',
                                  objid='1.1',
                                  period='830-910',
                                  dow='MO',
                                  student=self.student,
                                  modname=__name__)
        
    def test_(self):
        from types import StringType,IntType, UnicodeType
        expected_results = [[('pobjid', '1.1'), 
                             ('objid', 'booker'), 
                             ('objtype', 'Student'), 
                             ('nationality', 'british')], 
                            [('pobjid', 'ROOT'), 
                             ('period', '830-910'), 
                             ('dow', 'MO'), 
                             ('objid', '1.1'), 
                             ('objtype', 'Lesson')], 
                            [('pobjid', 'ROOT'), 
                             ('objid', 'booker'), 
                             ('objtype', 'Student'), 
                             ('nationality', 'british')]]

                
        _results = self.of.dumpobj()
        results = []
        for result in _results:
            result.pop('id')
            results.append([(k,v) for k,v in result.iteritems() if type(v) in [IntType,StringType,UnicodeType]])

        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
    def test_filter_on_lesson(self):
        
        # only report on the Lesson object (and its children)
        from types import StringType,IntType, UnicodeType
        
        expected_results = [[('pobjid', 'ROOT'), 
                             ('period', '830-910'), 
                             ('dow', 'MO'), 
                             ('objid', '1.1'), 
                             ('objtype', 'Lesson')]]


                
        _results = self.of.dumpobj(['Lesson'])
        results = []
        for result in _results:
            result.pop('id')
            results.append([(k,v) for k,v in result.iteritems() if type(v) in [IntType,StringType,UnicodeType]])

        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
    def test_filter_on_student(self):
        
        # only report on the Student object and its children
        from types import StringType,IntType, UnicodeType
        
        expected_results = [[('pobjid', 'ROOT'), 
                             ('objid', 'booker'), 
                             ('objtype', 'Student'), 
                             ('nationality', 'british')]]
                
        _results = self.of.dumpobj(['Student'])
        results = []
        for result in _results:
            result.pop('id')
            results.append([(k,v) for k,v in result.iteritems() if type(v) in [IntType,StringType,UnicodeType]])

        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
        
class Test_ObjFrameworkDumpNestedSchoolsched(unittest.TestCase):
    
    # same as above just with the school sched nested object
    # so each attr is another object of (not a string or int) that 
    # potentially needs to be accessed via accessors
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        datamembers = dict(period='830',
                           student='Booker',
                           dow='MO',
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
        
        
    def test_(self):
        from types import StringType,IntType, UnicodeType
            
        expected_results = [[('name', 0), ('pobjid', 'ROOT'), ('objid', 0), ('objtype', 'saveversion'), ('userobjid', 0)], 
                            [('name', 0), ('pobjid', 'dblesson0'), ('objid', 0), ('objtype', 'saveversion'), ('userobjid', 0)], 
                            [('name', '830'), ('pobjid', 'ROOT'), ('objid', '830'), ('objtype', 'period'), ('userobjid', '830')], 
                            [('name', '830'), ('pobjid', 'dblesson0'), ('objid', '830'), ('objtype', 'period'), ('userobjid', '830')], 
                            [('name', 'AM.AC.SC'), ('pobjid', 'ROOT'), ('objid', 'AM.AC.SC'), ('objtype', 'session'), ('userobjid', 'AM.AC.SC')], 
                            [('name', 'AM.AC.SC'), ('pobjid', 'dblesson0'), ('objid', 'AM.AC.SC'), ('objtype', 'session'), ('userobjid', 'AM.AC.SC')], 
                            [('name', 'Amelia'), ('pobjid', 'ROOT'), ('objid', 'Amelia'), ('objtype', 'teacher'), ('userobjid', 'Amelia')], 
                            [('name', 'Amelia'), ('pobjid', 'dblesson0'), ('objid', 'Amelia'), ('objtype', 'teacher'), ('userobjid', 'Amelia')], 
                            [('name', 'Booker'), ('pobjid', 'ROOT'), ('objid', 'Booker'), ('objtype', 'student'), ('userobjid', 'Booker')], 
                            [('name', 'Booker'), ('pobjid', 'dblesson0'), ('objid', 'Booker'), ('objtype', 'student'), ('userobjid', 'Booker')], 
                            [('name', 'MO'), ('pobjid', 'ROOT'), ('objid', 'MO'), ('objtype', 'dow'), ('userobjid', 'MO')],
                            [('name', 'MO'), ('pobjid', 'dblesson0'), ('objid', 'MO'), ('objtype', 'dow'), ('userobjid', 'MO')], 
                            [('pobjid', 'ROOT'), ('objid', 'dblesson0'), ('objtype', 'DBLesson')]]
        

        _results = self.of.dumpobj()
        results = []
        for result in _results:
            result.pop('id')
            results.append([(k,v) for k,v in result.iteritems() if type(v) in [IntType,StringType,UnicodeType]])

        expected_results.sort()
        results.sort()
        
        self.assertListEqual(expected_results,results)
        
    def test_filter_lesson(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results = [[('pobjid', 'ROOT'), ('objid', 'dblesson0'), ('objtype', 'DBLesson')]]
        
        _results = self.of.dumpobj(['DBLesson'])
        results = []
        for result in _results:
            result.pop('id')
            results.append([(k,v) for k,v in result.iteritems() if type(v) in [IntType,StringType,UnicodeType]])

        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
    def test_filter_lesson_student(self):
        
        # will only give children of lesson or student that are of type lesson or student
        from types import StringType,IntType, UnicodeType
            
        expected_results = [[('name', 'Booker'), ('pobjid', 'ROOT'), ('objid', 'Booker'), ('objtype', 'student'), ('userobjid', 'Booker')], 
                            [('name', 'Booker'), ('pobjid', 'dblesson0'), ('objid', 'Booker'), ('objtype', 'student'), ('userobjid', 'Booker')], 
                            [('pobjid', 'ROOT'), ('objid', 'dblesson0'), ('objtype', 'DBLesson')]]


        _results = self.of.dumpobj(['DBLesson','student'])
        results = []
        for result in _results:
            result.pop('id')
            results.append([(k,v) for k,v in result.iteritems() if type(v) in [IntType,StringType,UnicodeType]])

        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
        
class Test_ObjFrameworkDumpRpt(unittest.TestCase):
    
    def setUp(self):
        self.of = ObjFactory(True)
        self.obj1 = self.of.new(GenericBase,
                    'Student',
                    objid='booker',
                    nationality='british',
                    modname=__name__)
        
    def test_no_datafields(self):
        from types import StringType,IntType, UnicodeType
        expected_results = [['ROOT', 'Student']]

                
        results = self.of.dumpobjrpt(objref=False)
        
        expected_results.sort()
        results.sort()
        
        self.assertListEqual(expected_results,results)
        
    def test_inc_datafields(self):
        from types import StringType,IntType, UnicodeType
        expected_results = [['ROOT', 'british', 'Student']]

                
        results = self.of.dumpobjrpt(fields=['nationality'],objref=False)
        
        expected_results.sort()
        results.sort()
        
        self.assertListEqual(expected_results,results)
 
        
class Test_ObjFrameworkDumpRptNestedSchoolsched(unittest.TestCase):
    
    # same as above just with the school sched nested object
    # so each attr is another object of (not a string or int) that 
    # potentially needs to be accessed via accessors
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        datamembers = dict(period='830',
                           student='Booker',
                           dow='MO',
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
        
        
    def test_(self):
        from types import StringType,IntType, UnicodeType
        results = self.of.dumpobjrpt(objref=False)
        
        expected_results = [['ROOT', 'period'], 
                            ['ROOT', 'saveversion'], 
                            ['ROOT', 'dow'], 
                            ['dblesson0', 'dow'], 
                            ['dblesson0', 'period'], 
                            ['dblesson0', 'saveversion'], 
                            ['dblesson0', 'session'], 
                            ['dblesson0', 'student'], 
                            ['dblesson0', 'teacher'], 
                            ['ROOT', 'DBLesson'], 
                            ['ROOT', 'session'], 
                            ['ROOT', 'student'], 
                            ['ROOT', 'teacher']]
        
        self.assertListEqual(expected_results,results)

    def test_filter_objtype(self):
        from types import StringType,IntType, UnicodeType
        results = self.of.dumpobjrpt(objtypes=['DBLesson','student'],objref=False)
         
        expected_results = [['dblesson0', 'student'], 
                            ['ROOT', 'DBLesson'],
                            ['ROOT', 'student']]
        
        
        expected_results.sort()
        results.sort()
        
        self.assertListEqual(expected_results,results)
        
    def test_filter_objtype_3items(self):
        from types import StringType,IntType, UnicodeType
        results = self.of.dumpobjrpt(objtypes=['DBLesson','student','dow'],objref=False)
         
        expected_results = [['dblesson0', 'student'], 
                            ['ROOT', 'DBLesson'],
                            ['ROOT', 'student'],
                            ['dblesson0', 'dow'], 
                            ['ROOT', 'dow']] 
        
        
        expected_results.sort()
        results.sort()
        
        self.assertListEqual(expected_results,results)
        
    
    def test_filter_objtype_field_filters(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results = [['ROOT', '-', '-', 'student'], 
                            ['ROOT', 'Amelia', 'Booker', 'DBLesson'], 
                            ['dblesson0', '-', '-', 'student']]


        results = self.of.dumpobjrpt(objtypes=['DBLesson','student'],
                                     objref=False,
                                     fields=['teacher','student'])
         
        
        expected_results.sort()
        results.sort()
        
        self.assertListEqual(expected_results,results)
        

    def test_all_fields(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results = [['ROOT', 'dm:teacher=Amelia', 
                             'dm:session=AM.AC.SC', 'dm:student=Booker', 
                             'dm:period=830', 'dm:saveversion=0', 
                             'dm:dow=MO', 'dm:dm:dow=MO', 'dow:MO', 
                             'objid:dblesson0', 'period:830', 
                             'recursion:True', 'saveversion:0', 
                             'session:AM.AC.SC', 'student:Booker', 
                             'teacher:Amelia']]

        results = self.of.dumpobjrpt(objtypes=['DBLesson'],
                                     objref=False,
                                     fields=['all'],
                                     omitfields=['id'],
                                     fieldnames=True)
         
        
        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        

        
    def tearDown(self):
        self.of.reset()
        

class Test_ObjFrameworkDumpRptNestedSchoolschedConstraints(unittest.TestCase):
    
    # same as above just with the school sched nested object
    # so each attr is another object of (not a string or int) that 
    # potentially needs to be accessed via accessors
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        datamembers = dict(period='830-910',student='Booker',dow='MO',
                           teacher='Amelia',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson0',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
        
        
        datamembers = dict(period='910-950',student='Booker',dow='MO',
                           teacher='Stan',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson1',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
        

        datamembers = dict(period='950-1020',student='Booker',dow='MO',
                           teacher='Samantha',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson2',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
    

        datamembers = dict(period='830-910',student='Clayton',dow='MO',
                           teacher='Samantha',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson3',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
        

    def test_no_constraint(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results =[['ROOT', '-', 'DBLesson'], ['ROOT', '-', 'DBLesson'], 
                           ['ROOT', '-', 'DBLesson'], ['ROOT', '-', 'DBLesson'], 
                           ['ROOT', '0', 'saveversion'], ['ROOT', '830-910', 'period'], 
                           ['ROOT', '910-950', 'period'], ['ROOT', '950-1020', 'period'], 
                           ['ROOT', 'AM.AC.SC', 'session'], ['ROOT', 'Amelia', 'teacher'], 
                           ['ROOT', 'Booker', 'student'], ['ROOT', 'Clayton', 'student'], 
                           ['ROOT', 'MO', 'dow'], ['ROOT', 'Samantha', 'teacher'], 
                           ['ROOT', 'Stan', 'teacher'], ['dblesson0', '0', 'saveversion'],
                           ['dblesson0', '830-910', 'period'], ['dblesson0', 'AM.AC.SC', 'session'], 
                           ['dblesson0', 'Amelia', 'teacher'], ['dblesson0', 'Booker', 'student'],
                           ['dblesson0', 'MO', 'dow'], ['dblesson1', '0', 'saveversion'], 
                           ['dblesson1', '910-950', 'period'], ['dblesson1', 'AM.AC.SC', 'session'], 
                           ['dblesson1', 'Booker', 'student'], ['dblesson1', 'MO', 'dow'], 
                           ['dblesson1', 'Stan', 'teacher'], ['dblesson2', '0', 'saveversion'], 
                           ['dblesson2', '950-1020', 'period'], ['dblesson2', 'AM.AC.SC', 'session'], 
                           ['dblesson2', 'Booker', 'student'], ['dblesson2', 'MO', 'dow'], 
                           ['dblesson2', 'Samantha', 'teacher'], ['dblesson3', '0', 'saveversion'], 
                           ['dblesson3', '830-910', 'period'], ['dblesson3', 'AM.AC.SC', 'session'], 
                           ['dblesson3', 'Clayton', 'student'], ['dblesson3', 'MO', 'dow'], 
                           ['dblesson3', 'Samantha', 'teacher']]

        results = self.of.dumpobjrpt(objref=False,
                                     fields=['name'],
                                     omitfields=['id'])
         
        
        expected_results.sort()
        results.sort()

        #print results
        self.assertEqual(len(results),39)
        
    def test_1constraint(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results = [['ROOT', 'student:Booker', 'period:830-910', 'objtype:DBLesson'], 
                            ['ROOT', 'student:Clayton', 'period:830-910', 'objtype:DBLesson']]

        results = self.of.dumpobjrpt(objtypes=['DBLesson'],
                                     objref=False,
                                     fields=['student','period'],
                                     omitfields=['id'],
                                     fieldnames=True,
                                     constraints=dict(period=['830-910']))
         
        
        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
    def test_1constraint_multivals(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results = [['ROOT', 'student:Booker', 'period:830-910', 'objtype:DBLesson'], 
                            ['ROOT', 'student:Booker', 'period:950-1020', 'objtype:DBLesson'], 
                            ['ROOT', 'student:Clayton', 'period:830-910', 'objtype:DBLesson']]
        
        results = self.of.dumpobjrpt(objtypes=['DBLesson'],
                                     objref=False,
                                     fields=['student','period'],
                                     omitfields=['id'],
                                     fieldnames=True,
                                     constraints=dict(period=['830-910','950-1020']))
         
        
        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
    def test_1constraint_teacher(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results = [['ROOT', 'teacher:Stan', 'period:910-950', 'objtype:DBLesson']]
        
        results = self.of.dumpobjrpt(objtypes=['DBLesson'],
                                     objref=False,
                                     fields=['teacher','period'],
                                     omitfields=['id'],
                                     fieldnames=True,
                                     constraints=dict(teacher=['Stan']))
         
        
        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)
        
class Test_ObjFrameworkDumpRptNestedSchoolschedFieldNameHdr(unittest.TestCase):
    
    # same as above just with the school sched nested object
    # so each attr is another object of (not a string or int) that 
    # potentially needs to be accessed via accessors
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        datamembers = dict(period='830-910',student='Booker',dow='MO',
                           teacher='Amelia',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson0',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
        
        
        datamembers = dict(period='910-950',student='Booker',dow='MO',
                           teacher='Stan',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson1',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
        

        datamembers = dict(period='950-1020',student='Booker',dow='MO',
                           teacher='Samantha',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson2',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
    

        datamembers = dict(period='830-910',student='Clayton',dow='MO',
                           teacher='Samantha',saveversion=0,session='AM.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,'DBLesson',objid='dblesson3',constructor='datamembers',database=self.database,of=self.of,modname=__name__,dm=datamembers)
        
    def test_1constraint(self):
        from types import StringType,IntType, UnicodeType
        
        expected_results = [['ROOT', 'student:Booker', 'period:830-910', 'objtype:DBLesson'], 
                            ['ROOT', 'student:Clayton', 'period:830-910', 'objtype:DBLesson']]

        results = self.of.dumpobjrpt(objtypes=['DBLesson'],
                                     objref=False,
                                     fields=['student','period'],
                                     omitfields=['id'],
                                     C 1-on-1
G 1-on-1
A 1-on-1
E 1-on-1=True)
         
        
        expected_results.sort()
        results.sort()

        self.assertListEqual(expected_results,results)

        self.assertListEqual(expected_results,results)

class Test_ObjFrameworkGetByVal(unittest.TestCase):   
    # test we can find an return an object given the type and the value
    
    def setUp(self):
        self.of = ObjFactory(True)
        self.database = Database('foobar')
        
        datamembers = dict(period='830',
                           student='Booker',
                           dow='MO',
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
        
        datamembers = dict(period='910',
                           student='Clayton',
                           dow='TU',
                           teacher='Stan',
                           saveversion=0,
                           session='ST.AC.SC')

        self.foobar= self.of.new(schoolschedgeneric,
                                 'DBLesson',
                                 objid='dblesson1',
                                 constructor='datamembers',
                                 database=self.database,
                                 of=self.of,
                                 modname=__name__,
                                 dm=datamembers)
        
    def test_(self):

        self.assertEquals(self.of.object_get_byval("period","830").name,"830")        
        self.assertEquals(self.of.object_get_byval("period","910").name,"910")
        self.assertEquals(self.of.object_get_byval("period","foobar"),None)
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkBasic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDupeID))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_2_records_same_cls))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_2_class))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkIter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database_Derived))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database_Derived_Nested))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database_Derived_Nested_DupeKey))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFramework_Database_Derived_DB))'''
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDumpNested))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDump))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDumpNestedSchoolsched))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDumpRpt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDumpRptNestedSchoolsched))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkGetByVal))
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDumpRptNestedSchoolschedConstraints))
    
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ObjFrameworkDumpRptNestedSchoolschedFieldNameHdr))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
