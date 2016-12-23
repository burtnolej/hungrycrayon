import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest
import ssviewer_utils
import sswizard_utils
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
        database = Database(dbname)
        self.of = ObjFactory(True)
        enums = sswizard_utils.setenums(dow="all",prep=-1,database=database)
        
        args = dict(database=database,refdatabase=database,saveversion=1,of=self.of,enums=enums)
        
        ssviewer_utils.dataset_load(**args)

    def test_lesson(self):
        
        expected_results = {'status': u'master', 'recordtype': u'subject', 'period': u'1030-1110', 'substatus': u'complete', 'source': u'dbinsert', 'session': u'Dylan.Game Period.Monday.1030-1110', 'adult': u'Dylan', 'student': u'Clayton', 'id': u'00427CB0', 'objtype': 'lesson', 'dow': u'MO', 'userobjid': u'4.1.2.37.37', 'subject': u'Game Period'}
        
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
        
        '''
        need to put date on timestamp
        
        consider just marking original full record as "del"
           
        and added a complete new one
           
        use status field as "deleted"
        '''
    
class Test_addrecord(unittest.TestCase):
    
    def setUp(self):
        
        self.dbname='service_add_record'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        self.prepmap = sswizard_utils._loadprepmapper(self.database)

        args = dict(database=self.database,refdatabase=self.database,saveversion=1,of=self.of,enums=self.enums)
        ssviewer_utils.dataset_load(**args)

    def test_(self):
        
        expected_result = 'Stan.Math.Tuesday.830-910'
        
        datamembers = {'student':'Nathaniel',
                       'adult':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
    
        self.assertEqual(self.of.object_get('lesson',datamembers['userobjid']).session.name,
                         expected_result)
        

    def test_pivot(self):
        
        expected_result = [['', u'MO', u'TU'], [u'830-910', [], [('Math',)]], [u'1030-1110', [(u'Game Period',)], []]]

        datamembers = {'student':'Clayton',
                       'adult':'Stan',
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
        
        with self.database:
            newobj.persist()
            
            
    def test_dupe(self):
        
        expected_result = [['', u'MO', u'TU'], [u'830-910', [], [('Math',)]], [u'1030-1110', [(u'Game Period',)], []]]

        datamembers = {'student':'Clayton',
                       'adult':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        newobj = ssviewer_utils.dataset_add(**args)
        
        with self.assertRaises(Exception):
            newobj = ssviewer_utils.dataset_add(**args)
        
        
    def tearDown(self):
        shutil.copyfile(self.dbname+".sqlite.backup",self.dbname + ".sqlite")
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_getpage))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_getrecord))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_addrecord))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


