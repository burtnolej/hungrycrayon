import sys
import os
from os import path as ospath
from shutil import copyfile

from Tkinter import *
from ttk import *

import unittest
from shutil import copyfile

from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get

from misc_utils import nxnarraycreate
from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO
from sswizard_query_utils import *

from database_util import Database
from database_table_util import tbl_rows_get, tbl_query, tbl_remove

from sswizard_utils import dropdown_build, setenums, session_code_gen, dbinsert, dbinsert_direct, gridreduce
            
'''def _execfunc(database,value,prep):
    
    exec_str = "select s.code "
    exec_str += "from session as s,adult as a "
    exec_str += "where a.prep = {0} and ".format(prep)
    exec_str += "a.name = s.teacher and "
    exec_str += "s.period = {0} and ".format(value)
    exec_str += "a.subject <> \"None\""
    
    #exec_str = "select code from session where period = {0} and subject <> \"None\"".format(value)
    return(tbl_query(database,exec_str))

def _rowheaderexecfunc(database):
    exec_str = "select name from period"
    return(tbl_query(database,exec_str))

def _columnheaderexecfunc(database):
    exec_str = "select nickname from student"
    return(tbl_query(database,exec_str))'''

class UI(Tk):
    def __init__(self,database):       
        Tk.__init__(self)
        
        self.maxrows=9 # rows in the grid
        self.maxcols=10 # cols in the grid
        maxwidgets=self.maxrows*self.maxcols
        wwidth=48 # default button width with text of 3 chars
        wheight=29 # default button height
        wmheight=wheight*20 # master height
        wmwidth=wwidth*20 # master width 
    
        geom = geometry_get(wmheight,wmwidth,0,0)
        self.geometry(geom)
        
        widget_args=dict(background='white')
        
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        widgetcfg = dropdown_build(database,widgetcfg,
                                   _execfunc,
                                   _rowheaderexecfunc,
                                   _columnheaderexecfunc)

        setmemberp = SetMemberPartial(name='x{mylist}',set=[])

        self.entrygrid = TkImageLabelGrid(self,'entrygrid',setmemberp,wmwidth,wmheight,
                                          0,0,self.maxrows,self.maxcols,
                                          {},widgetcfg)
        self.entrygrid.grid(row=0,sticky=NSEW)      


class Test_With_Headers(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('test_sswizard_utils')
        self.classtbl = 'class'
        self.maxx = 8
        self.maxy = 10
        
        widget_args=dict(background='white')
    
        self.widgetcfg = nxnarraycreate(self.maxx+1,self.maxy+1,widget_args)
        self.widgetcfg = dropdown_build(self.database,
                                  self.widgetcfg,
                                   _execfunc,
                                   _rowheaderexecfunc,
                                   _columnheaderexecfunc)


    def test_col1(self):
        testx=0
       
        expected_results = ['Da-Hum','Br-STEM','Jk-Mvmt','Th-STEM','Js-Hum']
        self.assertEqual(self.widgetcfg[testx+1][1]['values'],expected_results)

    def test_col2(self):
        testx=7
       
        expected_results = ['Da-Hum','Br-STEM','Jk-AP']
        self.assertEqual(self.widgetcfg[testx+1][1]['values'],expected_results)
        
    def test_col7_rowheader(self):
        testx=7
        expected_results = ['830-920','920-1000','1000-1040','1040-1130','1240-1320',
                           '1320-1400','1400-1440','1440-1530']
       
        self.assertEqual(self.widgetcfg[testx+1][0]['values'],expected_results)

    def test_row1_colheader(self):
    
        expected_results = ['A3','B3','C3','D3','E3',
                            'F3','G3','H3','I3','J3','A4','B4',
                            'C4','D4','E4','F4','G4','H4','I4',
                            'J4']
       
        self.assertEqual(self.widgetcfg[0][1]['values'],expected_results)

 
class Test_Dropdown(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('test_sswizard_utils')
        self.classtbl = 'class'
        self.maxx = 8
        self.maxy = 10

    def test_col1(self):
        prep=5
        widget_args=dict(background='white')
        
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc,prep)
       
        expected_results =[u'DA.AC.HU', u'BR.AC.ST', u'JA.CO.MV', u'TH.AC.ST', u'JE.AC.HU']
        expected_results.sort()
        
        results = widgetcfg[1][1]['values']
        results.sort()
        
        self.assertListEqual(results,expected_results)

    def test_col2(self):
        prep =5
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc,prep)
        
        expected_results = [u'DA.AC.HU', u'BR.AC.ST',u'JA.??.WP']
        expected_results.sort()
        
        results = widgetcfg[1][2]['values']
        results.sort()
        
        self.assertListEqual(results,expected_results)
         
    def test_col3(self):
        prep=5
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc,prep)
        
        expected_results = [u'DA.AC.HU', u'BR.AC.ST', u'JA.??.SP', u'TH.AC.ST', u'JE.AC.HU']
        expected_results.sort()
        
        results = widgetcfg[1][3]['values']
        results.sort()
        
        self.assertEqual(results,expected_results)

    '''def test_col4(self):
        testx=3
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = [u'DA.PR.HU', u'BR.PR.ST', u'JA.??.SP', u'TH.AC.ST', u'JE.AC.HU']
        self.assertEqual(widgetcfg[testx+1][0]['values'],expected_results)

    def test_col5(self):
        testx=4
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = [u'DA.AC.HU', u'BR.AC.ST', u'JA.CO.MV']

        self.assertEqual(widgetcfg[testx+1][0]['values'],expected_results)

    def test_col6(self):
        testx=5
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = [u'DA.AC.HU', u'BR.AC.ST', u'JA.??.SP']
        self.assertEqual(widgetcfg[testx+1][0]['values'],expected_results)
    
    def test_col7(self):
        testx=6
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = [u'DA.AC.HU', u'BR.AC.ST']

        self.assertEqual(widgetcfg[testx+1][0]['values'],expected_results)'''
        
class Test_GetEnums(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('test_sswizard_utils')
        self.enums =  setenums('all','3',self.database)
        
    def test_prep3_students_name(self):

        expected_results = ['A','B','C','D','E','F','G','H','I','J','??']
        
        self.assertListEqual(expected_results,self.enums['student']['name'])

    def test_prep3_students_name2enum(self):
        
        expected_results = {'A':1,'B':2,'C':3,'D':4, \
                            'E':5,'F':6,'G':7,'H':8, \
                            'I':9,'J':10}
        
        self.assertEqual(expected_results,self.enums['student']['name2enum'])

    def test_prep3_get_code_name2code(self):
        
        expected_results = {'A':'AA','B':'BA','D':'DA','C':'CA', \
                            'E':'EA','F':'FA','G':'GA','H':'HA', \
                            'I':'IA','J':'JA','??':'??'}
        
        self.assertEqual(expected_results,self.enums['student']['name2code'])
        
        
class Test_DBLoader(unittest.TestCase):
    
    def setUp(self):
        
        self.database = Database('test_sswizard_utils')
        
        self.cols = ['col1','col2']
        self.rows = [['val1','val2']]
        
    def test_(self):
        
        dbinsert(self.database,'session2',self.rows,self.cols)
        
        with self.database:
            
            _,rows,_ = tbl_rows_get(self.database,'session2',self.cols)
        
            print rows
        
    def tearDown(self):
        copyfile("test_sswizard_utils.sqlite.backup","test_sswizard_utils.sqlite")

class Test_DBInsert_Direct(unittest.TestCase):
    def setUp(self):  

        #Test_Base.setUp(self)
        
        self.databasename = "test_ssloader"

        self.database = Database(self.databasename)
        
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        

    def test_session(self):
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', u'Simon A','1-on-1'], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', 'Liam','1-on-1']]
            
        
        expected_results =  [['Thea.STEM.Tuesday', 'Tuesday',7,'Thea', 'STEM'], 
                             ['Jess.Humanities.Wednesday', 'Wednesday',6, 'Jess','Humanities']]
            
        expected_results.sort()
        
        dbinsert_direct(self.database,records,'session','test')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',['code','dow','period','teacher','subject'])
        
        rows.sort()
         
        #print expected_results,rows
        
        self.assertListEqual(expected_results,rows)
        
    def test_lesson(self):
        
        records = [['100-140', 'TU', 'STEM', 'Thea', u'Simon A','1-on-1'], 
                  ['1210-100', 'WE', 'Humanities', 'Jess', 'Liam','1-on-1']]
            
        
        expected_results =  [['Simon A', 'TU','100-140','Thea', 'STEM','Thea.STEM.Tuesday','7.2.15'], 
                             ['Liam', 'WE','1210-100', 'Jess','Humanities','Jess.Humanities.Wednesday','6.4.24']]
        

        expected_results.sort()
        
        dbinsert_direct(self.database,records,'lesson','test')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',['student','dow','period','teacher','subject','session','userobjid'])
        
        rows.sort()
        
        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")
        
class Test_DBInsert_Direct_Convert_Input_Types(unittest.TestCase):
    # pass in dow code's instead of names and period enums not names
    def setUp(self):  

        #Test_Base.setUp(self)
        
        self.databasename = "test_ssloader"

        self.database = Database(self.databasename)
        
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        

    def test_session(self):
        
        records = [[7, 'TU', 'STEM', 'Thea', u'Simon A','1-on-1'], 
                  [6, 'WE', 'Humanities', 'Jess', 'Liam','1-on-1']]
            
        
        expected_results =  [['Thea.STEM.Tuesday', 'Tuesday',7,'Thea', 'STEM'], 
                             ['Jess.Humanities.Wednesday', 'Wednesday',6, 'Jess','Humanities']]
            
        expected_results.sort()
        
        dbinsert_direct(self.database,records,'session','test')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',['code','dow','period','teacher','subject'])
        
        rows.sort()
         
        #print expected_results,rows
        
        self.assertListEqual(expected_results,rows)
        
    def test_lesson(self):
        
        records = [[7, 'Tuesday', 'STEM', 'Thea', u'Simon A','1-on-1'], 
                  [6, 'Wednesday', 'Humanities', 'Jess', 'Liam','1-on-1']]
            
        
        expected_results =  [['Simon A', 'TU','100-140','Thea', 'STEM','Thea.STEM.Tuesday'], 
                             ['Liam', 'WE','1210-100', 'Jess','Humanities','Jess.Humanities.Wednesday']]
        

        expected_results.sort()
        
        dbinsert_direct(self.database,records,'lesson','test')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',['student','dow','period','teacher','subject','session'])
        
        rows.sort()
        
        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")
    

class Test_GridReduce(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_1blankcol_1blankrow_space(self):
        
        self.grid = [['','A','B','C'],
                     ['X','','',''],
                     ['Y','foo','',''],
                     ['Z','','','bar']]    

        self.expected_results = [['','A','C'],
                               ['Y','foo',''],
                               ['Z','','bar']]     
        
        gridreduce(self.grid,[""])
        self.assertListEqual(self.grid,self.expected_results)
        
    def test_1blankcol_1blankrow_list(self):
        
        self.grid = [['','A','B','C'],
                     ['X',[],[],[]],
                     ['Y','foo',[],[]],
                     ['Z',[],[],'bar']]    

        self.expected_results = [['','A','C'],
                                 ['Y','foo',[]],
                                 ['Z',[],'bar']]     
        
        gridreduce(self.grid,[[]])
        self.assertListEqual(self.grid,self.expected_results)
        
    def test_allblank_list(self):
        
        self.grid = [['','A','B','C'],
                     ['X',[],[],[]],
                     ['Y',[],[],[]],
                     ['Z',[],[],[]]
                     ]

        self.expected_results = [['']]
        
        gridreduce(self.grid,[[]])
        self.assertListEqual(self.grid,self.expected_results)
        
    def test_noblank_list(self):
        
        import copy
        
        self.grid = [['','A','B','C'],
                     ['X',['blah'],['blah'],['blah']],
                     ['Y',['foo'],['blah'],['blah']],
                     ['Z',['blah'],['blah'],['bar']]]
        
        self.expected_results = copy.deepcopy(self.grid)
        
        gridreduce(self.grid,[[]])
        self.assertListEqual(self.grid,self.expected_results)

if __name__ == "__main__":
    suite = unittest.TestSuite()

    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_GridReduce))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Dropdown))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_With_Headers))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_GetEnums))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader))
    
    # dbinsert_direct
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBInsert_Direct))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBInsert_Direct_Convert_Input_Types))
    
unittest.TextTestRunner(verbosity=2).run(suite) 


