import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest
import ssviewer_utils
import sswizard_utils
import sswizard_query_utils
import shutil

from misc_utils_objectfactory import ObjFactory

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

class Test_getpage(unittest.TestCase):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        
        self.grid = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q']
        
    def test_(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,4)
        
    def test_page2(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,2)
        
        self.assertEqual(srow,5)
        self.assertEqual(erow,9)
        
    def test_page_last(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,4)
        
        self.assertEqual(srow,15)
        self.assertEqual(erow,16)
        
    def test_numrows_less_than1page(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,20,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,16)
        
    def test_page_too_high(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,5)
        
        self.assertEqual(srow,12)
        self.assertEqual(erow,16)
        
    def test_pagelen_2(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,2,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,2)
        
    def test_pagelen_2(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,2,2)
        
        self.assertEqual(srow,2)
        self.assertEqual(erow,3)
        
    def test_1sourcerow(self):
        
        srow,erow = ssviewer_utils._getpage(['a'],30,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,0)
        
class Test_getrecord(unittest.TestCase):
    
    def setUp(self):
        
        dbname='service_getrecord_1lesson'
        self.database = Database(dbname)
        self.of = ObjFactory(True)
        enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        
        args = dict(database=self.database,refdatabase=self.database,saveversion=1,
                    of=self.of,enums=enums)
        
        ssviewer_utils.dataset_load(**args)

    def test_lesson(self):
        
        expected_results = {'status': u'master', 'substatus': u'complete', 'recordtype': u'subject', 'period': u'1030-1110', 'dow': u'MO', 'source': u'dbinsert', 'session': u'Dylan.Game Period.Monday.1030-1110', 'adult': u'Dylan', 'student': u'Clayton', 'id': u'00427CB0', 'objtype': 'lesson', 'prep': 5, 'userobjid': u'4.1.2.37.37', 'subject': u'Game Period'}
        results = ssviewer_utils.dataset_record(self.of,'lesson','4.1.2.37.37')
                
        self.assertEqual(expected_results,results)
        
    def test_lesson_notfound(self):
        
        expected_results = {}
        
        results = ssviewer_utils.dataset_record(self.of,'lesson','4.1.3.37.37')
        
        self.assertEqual(expected_results,results)
        
    def test_subject(self):
        
        expected_results = {'objtype': 'subject', 'name': u'Game Period', 'userobjid': u'Game Period'}
        
        results = ssviewer_utils.dataset_record(self.of,'subject','Game Period')
        
        self.assertEqual(expected_results,results)
        
    def test_with_idlookup(self):
        
        expected_results = {'status': u'master', 'substatus': u'complete', 
                            'recordtype': u'subject', 'period': u'1030-1110', 
                            'dow': u'MO', 'source': u'dbinsert', 
                            'session': u'Dylan.Game Period.Monday.1030-1110', 
                            'adult': u'Dylan', 'student': u'Clayton', 'id': u'00427CB0', 
                            'objtype': 'lesson', 'prep': 5, 'userobjid': u'4.1.2.37.37', 
                            'subject': u'Game Period'}
        
        with self.database:
            dbidlookup = sswizard_query_utils._dbid2userdefid(self.database,asdict=True)

        dbid = dbidlookup["00427CB0"]
        
        results = ssviewer_utils.dataset_record(self.of,'lesson',dbid)
        
        self.assertEqual(expected_results,results)
    
class Test_addrecord(unittest.TestCase):
    
    def setUp(self):
        
        self.dbname='service_add_record'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        self.prepmap = sswizard_utils._loadprepmapper(self.database)

        args = dict(database=self.database,refdatabase=self.database,saveversion=1,of=self.of,enums=self.enums)
        ssviewer_utils.dataset_load(**args)

    '''def test_(self):
        
        expected_result = 'Stan.Math.Tuesday.830-910'
        
        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
    
        self.assertEqual(self.of.object_get('lesson',datamembers['userobjid']).session.name,
                         expected_result)'''
        
        
    '''def test_internal_dict(self):
        
        expected_result = {'status': 'complete', 'recordtype': 'subject', 'enum': 665, 
                           'period': '830-910', 'saveversion': 1, 'prep': 5, 'source': 'manual', 
                           'session': 'Stan.Math.Tuesday.830-910', 'adult': 'Stan', 'student': 'Nathaniel', 
                           'objtype': 'lesson', 'dow': u'TU', 'userobjid': '1.2.1.2.4', 'subject': 'Math'}

        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
    
        obj = self.of.object_get('lesson',datamembers['userobjid'])
                                 
        self.assertEqual(obj.dm,expected_result)'''
        
    def test_db(self):
        
        expected_result = [[u'Dylan', u'Clayton', u'1030-1110', u'MO', u'Game Period', u'subject'], 
                           [u'Stan', u'Nathaniel', u'830-910', u'TU', u'Math', u'subject']]


        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        obj = ssviewer_utils.dataset_add(**args)

        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',['teacher','student','period','dow','subject','recordtype','__id'])
         
        
        
        self.assertListEqual(expected_result,rows)
        
    '''def test_pivot(self):
        
        expected_result = [['', u'MO', u'TU'], [u'830-910', [], [('Math',)]], [u'1030-1110', [(u'Game Period',)], []]]

        datamembers = {'student':'Clayton',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        newobj = ssviewer_utils.dataset_add(**args)
        
        
        args = dict(of=self.of,enums=self.enums,
                    yaxis_type='dow',xaxis_type='period',
                    source_type='student',source_value='Clayton',
                    ztypes=['subject'])
                    
        result = ssviewer_utils.dataset_pivot(**args)
    
        self.assertListEqual(result,expected_result)
            
    def test_dupe(self):
        
        expected_result = [['', u'MO', u'TU'], [u'830-910', [], [('Math',)]], [u'1030-1110', [(u'Game Period',)], []]]

        datamembers = {'student':'Clayton',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        newobj = ssviewer_utils.dataset_add(**args)
        
        with self.assertRaises(Exception):
            newobj = ssviewer_utils.dataset_add(**args)'''
        
        
    def tearDown(self):
        shutil.copyfile(self.dbname+".sqlite.backup",self.dbname + ".sqlite")
        
class Test_addrecord_refdata(unittest.TestCase):
    
    ''' for adding non lesson records '''
    
    def setUp(self):
        
        self.dbname='service_add_record'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        self.prepmap = sswizard_utils._loadprepmapper(self.database)

        args = dict(database=self.database,refdatabase=self.database,saveversion=1,of=self.of,enums=self.enums)
        ssviewer_utils.dataset_load(**args)

    def test_add_period_db(self):
        
        expected_result = [[u'330-400']]
        
        objtype = 'period'
        datamembers = {'name':'330-400'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"period",['name'],[["name","=","\"330-400\""]])
    
        self.assertEqual(rows,expected_result)
        
        
    def test_add_period_object(self):
        
        expected_result = [[u'330-400']]

        objtype = 'period'
        datamembers = {'name':'330-400'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        newobj = ssviewer_utils.dataset_add(**args)
        
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"period",['name'],[["name","=","\"330-400\""]])
            
        self.assertEqual(rows,expected_result)
        
        expected_result = {'objtype': 'period', 'name': '330-400', 'userobjid': '330-400'}
        self.assertEqual(newobj.dm,expected_result)
        
    '''def test_add_dow(self):
        
        expected_result = [[u'Monday', u'MO', u'1'], [u'Tuesday', u'TU', u'2'], [u'Thursday', u'TH', u'3'], 
                           [u'Wednesday', u'WE', u'4'], [u'Friday', u'FR', u'5'], [u'XX', u'Foobarday', u'6']]

        objtype = 'dow'
        datamembers = {'name':'XX',
                       'code':'Foobarday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"dow",['name','code','enum'])

        self.assertEqual(rows,expected_result)
        
    def test_add_student(self):
        
        expected_result = [[u'Jon', u'JB', u'29']]

        objtype = 'student'
        datamembers = {'name':'Jon',
                       'code':'JB',
                       'prep':5}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"student",['name','code','enum'],[["name","=","\"Jon\""]])

        self.assertEqual(rows,expected_result)
        
    def test_add_adult(self):
        
        expected_result = [[u'Jon', u'JB', u'39']]

        objtype = 'adult'
        datamembers = {'name':'Jon',
                       'code':'JB',
                       'prep':5}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"adult",['name','code','enum'],[["name","=","\"Jon\""]])

        self.assertEqual(rows,expected_result)
        
    def test_add_subject(self):
        
        expected_result = [[u'Jon', u'JB', u'38']]

        objtype = 'subject'
        datamembers = {'name':'Jon',
                       'code':'JB',
                       'lessontype':'ap'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"subject",['name','code','enum'],[["name","=","\"Jon\""]])

        self.assertEqual(rows,expected_result)'''
        
    def tearDown(self):
        shutil.copyfile(self.dbname+".sqlite.backup",self.dbname + ".sqlite")
        

class Test_newrecord(unittest.TestCase):
    
    def setUp(self):
        
        self.dbname='test_service_new_record'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        self.prepmap = sswizard_utils._loadprepmapper(self.database)

        args = dict(database=self.database,refdatabase=self.database,saveversion=1,of=self.of,enums=self.enums)
        ssviewer_utils.dataset_load(**args)

    def test_(self):
    
        expected_result = {'adult':"",'subject':"",'dow':"",'period':"",'student':"",
                           'recordtype':""}
        
        result = ssviewer_utils.dataset_new('lesson')
    
        self.assertEqual(result,expected_result)
        
        
class Test_dump(unittest.TestCase):
    
    def setUp(self):
        
        self.dbname='test_ssviewer_rest_dump'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        self.prepmap = sswizard_utils._loadprepmapper(self.database)

        args = dict(database=self.database,refdatabase=self.database,saveversion=1,of=self.of,enums=self.enums)
        ssviewer_utils.dataset_load(**args)

    def test_(self):
        
        expected_results = [[u'1.2.2.6.22', '-', '-', 'subject'], 
                            ['ROOT', u'Amelia', u'Clayton', 'lesson'], 
                            ['ROOT', '-', '-', 'subject']]
        
        result = self.of.dumpobjrpt(objtypes=['lesson','subject'],objref=False,
                                    fields=['adult','student'])
        
        self.assertListEqual(result,expected_results)
        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_getpage))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_getrecord))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_addrecord))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_addrecord_refdata))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_newrecord))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_dump))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


