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
        
        expected_results = {'status': u'master', 'substatus': u'complete', 'recordtype': u'academic', 'period': u'1030-1110', 'dow': u'MO', 'source': u'dbinsert', 'session': u'Dylan.Game Period.Monday.1030-1110', 'adult': u'Dylan', 'student': u'Clayton', 'id': u'00427CB0', 'objtype': 'lesson', 'prep': 5, 'userobjid': u'4.1.2.37.37', 'subject': u'Game Period'}
        results = ssviewer_utils.dataset_record(self.of,'lesson','4.1.2.37.37')
                
        self.assertEqual(expected_results,results)
        
    def test_lesson_notfound(self):
        
        expected_results = {}
        
        results = ssviewer_utils.dataset_record(self.of,'lesson','4.1.3.37.37')
        
        self.assertEqual(expected_results,results)
        
    def test_subject(self):
        
        expected_results = {'code': u'Game Period', 
                            'name': u'Game Period', 
                            'enum': 0, 
                            'objtype': 'subject', 
                            'userobjid': u'Game Period'}
        
        results = ssviewer_utils.dataset_record(self.of,'subject','Game Period')
        
        results.pop('id')
        
        self.assertEqual(expected_results,results)
        
    def test_with_idlookup(self):
        
        expected_results = {'status': u'master', 'substatus': u'complete', 
                            'recordtype': u'academic', 'period': u'1030-1110', 
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
    
class Test_add_update(unittest.TestCase):
    
    def setUp(self):
        
        self.dbname='service_add_record'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        self.prepmap = sswizard_utils._loadprepmapper(self.database)

        args = dict(database=self.database,refdatabase=self.database,saveversion=1,of=self.of,enums=self.enums)
        ssviewer_utils.dataset_load(**args) 
        
    def test_update_add(self):

        # check that a record can be updated after it has been added
        expected_results = [['status', 'substatus', 'recordtype', 'period', 'dow', 'source', 'session', 'adult', 'student', 'id', 'objtype', 'prep', 'userobjid', 'subject'], 
                            [u'master', u'complete', u'academic', u'1030-1110', u'MO', u'dbinsert', u'Dylan.Game Period.Monday.1030-1110', u'Dylan', u'Clayton', 'lesson', 5, u'4.1.2.37.37', u'Game Period'], 
                            ['master', 'complete', 'academic', '1030-1110', u'TU', 'manual', 'Stan.Math.Tuesday.830-910', 'Stan', 'Nathaniel', 'lesson', 5, '1.2.1.2.4', 'Math']]

        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'academic',
                       'dow':'Tuesday'}

        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers,keepversion=True)

        obj = ssviewer_utils.dataset_add(**args)

        obj.keepversion=True
        obj.customtimestamp = "%y%m%d_%H%M%S"
        newid = obj.update(self.of,'period','1030-1110',self.dbname)

        grid,colnames = ssviewer_utils.dataset_list(self.of,self.enums,columns=['status', 'substatus', 'recordtype', 'period', 'dow', 'source', 'session', 'adult', 'student', 'objtype', 'prep', 'userobjid', 'subject'])

        self.assertListEqual(grid,expected_results)

        # tests whats in the database
        expected_results = [[u'Dylan', u'Clayton', u'1030-1110', u'MO', u'Game Period', u'academic', u'current', u'master', u'complete', u'dbinsert'], 
                            [u'Stan', u'Nathaniel', u'830-910', u'TU', u'Math', u'academic', u'version', u'master', u'complete', u'manual'], 
                            [u'Stan', u'Nathaniel', u'1030-1110', u'TU', u'Math', u'academic', u'current', u'master', u'complete', u'manual']]
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',['teacher','student','period','dow','subject','recordtype','__version','status','substatus','source'])

        self.assertListEqual(rows,expected_results)
    
    
    def tearDown(self):
        pass
        shutil.copyfile(self.dbname+".sqlite.backup",self.dbname + ".sqlite")
    
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
        
        # test that a new object is added into of store with the correct userobjid
        
        expected_result = 'Stan.Math.Tuesday.830-910'
        
        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'academic',
                       'dow':'Tuesday'}
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
    
        self.assertEqual(self.of.object_get('lesson',datamembers['userobjid']).session.name,
                         expected_result)
        
    def test_internal_dict(self):
        
        # test that the internal datamembers/dm dict has the correct keys by asserting correct values
        # and comparing keys vs a recovered record
        
        expected_result = {'status': 'master', 'prep': 5, 'recordtype': 'subject', 
                           'period': '830-910', 'substatus': 'complete', 'source': 'manual', 'session': 
                           'Stan.Math.Tuesday.830-910', 'adult': 'Stan', 'student': 'Nathaniel', 'objtype': 
                           'lesson', 'dow': u'TU', 'userobjid': '1.2.1.2.4', 'subject': 'Math'} 
        
        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
    
        obj_recovered = self.of.query('lesson')[0].dm.keys()
        obj_add = self.of.query('lesson')[1].dm.keys()
             
        obj_recovered.sort()
        obj_add.sort()
        
        # test keys
        self.assertListEqual(obj_recovered,obj_add)
        
        obj = self.of.object_get('lesson',datamembers['userobjid'])
            
        obj.dm.pop("id")
        
        # test values
        self.assertEqual(obj.dm,expected_result)
        
    def test_internal_attr(self):
        
        # check the member attr values and that the keys are the same between recovered and added objects
        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'subject',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        obj = ssviewer_utils.dataset_add(**args)
        
        self.assertEquals(obj.adult.name,'Stan')
        self.assertEquals(obj.dow.name,'TU')
        self.assertTrue(hasattr(obj,'id'))
        self.assertEquals(obj.objtype.name,'lesson')
        self.assertEquals(obj.period.name,'830-910')
        self.assertEquals(obj.prep.name,5)
        self.assertEquals(obj.recordtype.name,'subject')
        self.assertEquals(obj.session.name,'Stan.Math.Tuesday.830-910')
        self.assertEquals(obj.source.name,'manual')
        self.assertEquals(obj.status.name,'master')
        self.assertEquals(obj.student.name,'Nathaniel')
        self.assertEquals(obj.subject.name,'Math')
        self.assertEquals(obj.substatus.name,'complete')
        self.assertEquals(obj.userobjid.name,'1.2.1.2.4')

        obj_addattrnames = [k for k,v in obj.attr_get_keyval(include_callable=False,
                                       include_nondataattr=False)]
        
        obj_recoveredattrnames = [k for k,v in self.of.query('lesson')[0].attr_get_keyval(include_callable=False,
                                       include_nondataattr=False)]
        
        self.assertListEqual(obj_addattrnames, obj_recoveredattrnames) 
        
    def test_db(self):
        
        expected_result = [[u'Dylan', u'Clayton', u'1030-1110', u'MO', u'Game Period', u'academic'], 
                           [u'Stan', u'Nathaniel', u'830-910', u'TU', u'Math', u'academic']]

        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'academic',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers)
    
        obj = ssviewer_utils.dataset_add(**args)
        obj.keepversion=True
        obj.customtimestamp = "%y%m%d_%H%M%S"

        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',['teacher','student','period','dow','subject','recordtype'])
         
        self.assertListEqual(expected_result,rows)
        
    def test_db_updates_enabled(self):
        
        expected_result = [[u'Dylan', u'Clayton', u'1030-1110', u'MO', u'Game Period', u'academic','current'], 
                           [u'Stan', u'Nathaniel', u'830-910', u'TU', u'Math', u'academic','current']]

        datamembers = {'student':'Nathaniel',
                       'teacher':'Stan',
                       'subject':'Math',
                       'period':'830-910',
                       'recordtype':'academic',
                       'dow':'Tuesday'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    datamembers=datamembers,keepversion=True)
    
        obj = ssviewer_utils.dataset_add(**args)
        obj.keepversion=True
        obj.customtimestamp = "%y%m%d_%H%M%S"

        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',['teacher','student','period','dow','subject','recordtype','__version'])
         
        self.assertListEqual(expected_result,rows)
        
    def test_pivot(self):
        
        expected_result = [['', u'MO', u'TU'], [u'1030-1110', [(u'Game Period',)], []], ['830-910', [], [('Math',)]]]
        
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
            newobj = ssviewer_utils.dataset_add(**args)
        
        
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
        datamembers = {'name':'330-400','code':'330'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"period",['name'],[["name","=","\"330-400\""]])
    
        self.assertEqual(rows,expected_result)
        
        
    def test_add_period_object(self):
        
        expected_result = [[u'330-400']]
        
        objtype = 'period'
        datamembers = {'name':'330-400','code':'330'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        newobj = ssviewer_utils.dataset_add(**args)
        
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"period",['name'],[["name","=","\"330-400\""]])
            
        self.assertEqual(rows,expected_result)
        
        expected_result = {'code': '330', 'name': '330-400', 'enum': 11, 'objtype': 'period','userobjid': '330-400'}
        
        newobj.dm.pop('id')
        
        #print newobj.dm,expected_result
        self.assertEqual(newobj.dm,expected_result)
        
    def test_add_dow(self):
        
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
        
        expected_result = [[u'Cycling', u'CYCL', u'38']]
        
        objtype = 'subject'
        datamembers = {'name':'Cycling',
                       'code':'CYCL'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        obj = ssviewer_utils.dataset_add(**args)

        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"subject",['name','code','enum'],[["name","=","\"Cycling\""]])

        self.assertEqual(rows,expected_result)
        
        
    def test_add_subject_object(self):
        
        expected_result = [['code', 'name', 'enum', 'objtype', 'id', 'userobjid'], 
                           [u'Game Period', u'Game Period', 0, 'subject', u'Game Period'], 
                           ['CYCL', 'Cycling', 38, 'subject', 'Cycling']]

        objtype = 'subject'
        datamembers = {'name':'Cycling',
                       'code':'CYCL'}
        
        args = dict(database=self.database,refdatabase=self.database,prepmap=self.prepmap,of=self.of,enums=self.enums,
                    objtype=objtype,datamembers=datamembers)
    
        ssviewer_utils.dataset_add(**args)
        
        result,_ = ssviewer_utils.dataset_list(self.of,self.enums,'subject',pagelen=30,pagenum=1,
                                             constraints=[],columns=['code','name','enum','objtype','userobjid'])      
        
        self.assertListEqual(result,expected_result)
        
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
        
        
class Test_update(unittest.TestCase):
    
    def setUp(self):
        
        self.dbname='test_ssviewer_util_add'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        self.enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        self.prepmap = sswizard_utils._loadprepmapper(self.database)

        args = dict(database=self.database,refdatabase=self.database,saveversion=1,
                    of=self.of,enums=self.enums,keepversion=True)
        ssviewer_utils.dataset_load(**args)

    def test_update_subject(self):

        expected_results = [[u'master', u'complete', u'academic', u'830-910', u'WE', u'dbinsert', u'[Dylan,Francisco].Movement.Wednesday.830-910', u'[Dylan,Francisco]', u'Nathaniel', 5, u'1.4.1.None.8', u'Movement'], 
                            [u'master', u'complete', u'academic', u'830-910', u'WE', u'dbinsert', u'[Dylan,Francisco].Movement.Wednesday.830-910', u'[Dylan,Francisco]', u'Nathaniel', 5, u'1.4.1.None.8', u'ELA']]
        
        obj = self.of.query_advanced("lesson",[('period','830-910'),
                                          ('dow','WE')])
        
        obj[0].update(self.of,'subject','ELA')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"lesson",
                                    fields = ['status', 'substatus', 'recordtype', 'period', 'dow', 'source', 'session', 'teacher', 'student', 'prep', 'userobjid', 'subject'],
                                    whereclause = [["period","=","\"830-910\""],
                                                   ["dow","=","\"WE\""]])
            
        self.assertListEqual(rows,expected_results)


    def test_update_adult(self):
        
        expected_results = [[u'master', u'complete', u'academic', u'830-910', u'WE', u'dbinsert', u'[Dylan,Francisco].Movement.Wednesday.830-910', u'[Dylan,Francisco]', u'Nathaniel', 5, u'1.4.1.None.8', u'Movement'], 
                            [u'master', u'complete', u'academic', u'830-910', u'WE', u'dbinsert', u'[Dylan,Francisco].Movement.Wednesday.830-910', u'Amelia', u'Nathaniel', 5, u'1.4.1.None.8', u'Movement']]
        
        obj = self.of.query_advanced("lesson",[('period','830-910'),
                                          ('dow','WE')])
        
        obj[0].update(self.of,'teacher','Amelia')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,"lesson",
                                    fields = ['status', 'substatus', 'recordtype', 'period', 'dow', 'source', 'session', 'teacher', 'student', 'prep', 'userobjid', 'subject'],
                                    whereclause = [["period","=","\"830-910\""],
                                                   ["dow","=","\"WE\""]])
            
        self.assertListEqual(rows,expected_results)
        
    def tearDown(self):
        shutil.copyfile(self.dbname+".sqlite.backup",self.dbname + ".sqlite")
        
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
        
    def tearDown(self):
        shutil.copyfile(self.dbname+".sqlite.backup",self.dbname + ".sqlite")
        
        
        
class Test_load(unittest.TestCase):
            
    def setUp(self):
        
        dbname='service_getrecord_1lesson'
        self.database = Database(dbname)
        self.of = ObjFactory(True)
        enums = sswizard_utils.setenums(dow="all",prep=-1,database=self.database)
        
        args = dict(database=self.database,refdatabase=self.database,saveversion=1,
                    of=self.of,enums=enums)
        
        ssviewer_utils.dataset_load(**args)
              
    def test_(self):
        
        grid,_ = ssviewer_utils.dataset_list(of=self.of,
                                          objtype='period',pagelen=30,
                                          pagenum=1)
        
        print grid
        
        
class Test_loadref(unittest.TestCase):
    
    def setUp(self):
        
        self.dbname='test_ssviewer_util_add'
        self.database = Database(self.dbname)
        self.of = ObjFactory(True)
        
    def test_period(self):
        
        grid,colnames = ssviewer_utils.dataset_list(of=self.of,
                                            objtype='period',pagelen=30,
                                            pagenum=1,columns=['code','name','enum'])
        
        self.assertListEqual(grid,[])
       
        
        args = dict(database=self.database,refdatabase=self.database,
                    objtype='period',saveversion=1,
                    of=self.of,keepversion=True)
        ssviewer_utils.dataset_loadref(**args)

        expected_results = [['objtype', 'userobjid', 'code', 'name', 'enum'], 
                            [u'830', u'830-910', u'1'], 
                            [u'910', u'910-950', u'2'], 
                            [u'950', u'950-1030', u'3'], 
                            [u'1030', u'1030-1110', u'4'], 
                            [u'1110', u'1110-1210', u'5'], [u'1210', u'1210-1250', u'6'], [u'1310', u'1250-130', u'7'], [u'1340', u'130-210', u'8'], [u'1420', u'210-250', u'9'], 
                            [u'1500', u'250-310', u'10']]
        grid,_ = ssviewer_utils.dataset_list(of=self.of,
                                          objtype='period',pagelen=30,
                                          pagenum=1,
                                          columns=['code','name','enum'])

        self.assertListEqual(grid,expected_results)
        
            
    def test_student(self):
        
        grid,colnames = ssviewer_utils.dataset_list(of=self.of,
                                            objtype='student',pagelen=30,
                                            pagenum=1,columns=['code','name','enum','prep'])
        
        self.assertListEqual(grid,[])
       
        
        args = dict(database=self.database,refdatabase=self.database,
                    objtype='student',saveversion=1,
                    of=self.of,keepversion=True,
                    whereclause=[['name','=',"\"Nathaniel\""]])
        ssviewer_utils.dataset_loadref(**args)

        expected_results = [['code', 'name', 'enum', 'objtype', 'prep', 'userobjid'], 
                            [u'NATH', u'Nathaniel', u'1', u'5']] 
        
        grid,_ = ssviewer_utils.dataset_list(of=self.of,
                                          objtype='student',pagelen=30,
                                          pagenum=1,columns=['code','name','enum','prep'])
        
        self.assertListEqual(grid,expected_results)
    
    def tearDown(self):
        shutil.copyfile(self.dbname+".sqlite.backup",self.dbname + ".sqlite")
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_getpage))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_getrecord))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_addrecord))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_add_update))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_addrecord_refdata))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_newrecord))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_dump))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_update))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_load))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_loadref))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


