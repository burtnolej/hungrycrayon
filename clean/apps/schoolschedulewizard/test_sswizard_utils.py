import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from Tkinter import *
from ttk import *

import unittest

from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get

from misc_utils import nxnarraycreate
from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO

from database_util import Database
from database_table_util import tbl_rows_get, tbl_query

from sswizard_utils import dropdown_build, setenums
            
def _execfunc(database,value):
    exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(value)
    return(tbl_query(database,exec_str))

def _rowheaderexecfunc(database):
    exec_str = "select name from period"
    return(tbl_query(database,exec_str))

def _columnheaderexecfunc(database):
    exec_str = "select nickname from student"
    return(tbl_query(database,exec_str))

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
        
        self.database = Database('quadref')
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

 
class Test_(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('quadref')
        self.classtbl = 'class'
        self.maxx = 8
        self.maxy = 10

    def test_col1(self):
        testx=0
        widget_args=dict(background='white')
        
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
       
        expected_results = ['Da-Hum','Br-STEM','Jk-Mvmt','Th-STEM','Js-Hum']
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)

    def test_col2(self):
        testx=1
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = ['Da-Hum','Br-STEM']
        
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)
         
    def test_col3(self):
        testx=2
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-SPED','Th-STEM','Js-Hum']
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)

    def test_col4(self):
        testx=3
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = ['Jk-SPED','Th-STEM','Js-Hum']
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)

    def test_col5(self):
        testx=4
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-Mvmt']
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)

    def test_col6(self):
        testx=5
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-SPED']
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)
    
    def test_col7(self):
        testx=6
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = ['Da-Hum','Br-STEM']
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)

    def test_col8(self):
        
        testx=7
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(self.maxx,self.maxy,widget_args)
        exec_str = "select tag from class where period = {0} and subject <> \"None\"".format(testx+1)
        widgetcfg = dropdown_build(self.database,widgetcfg,_execfunc)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-AP']
        self.assertEqual(widgetcfg[testx][0]['values'],expected_results)

class Test_UI(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('quadref')
        self.ui = UI(self.database)
        
    def test_(self):
        
        print self.ui.entrygrid.widgets[0][0]['values']
        self.ui.mainloop()
        #pass
        
class Test_GetEnums(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('quadref_test')
        self.enums =  setenums('All','3','quadref_test')
        
    def test_prep3_students_name(self):

        expected_results = ['A','B','D','C','E','F','G','H','I','J']
        
        self.assertListEqual(expected_results,self.enums['student']['name'])

    def test_prep3_students_name2enum(self):
        
        expected_results = {'A':0,'B':1,'D':2,'C':3, \
                            'E':4,'F':5,'G':6,'H':7, \
                            'I':8,'J':9}
        
        self.assertEqual(expected_results,self.enums['student']['name2enum'])

    def test_prep3_get_code_name2code(self):
        
        expected_results = {'A':'AA','B':'BA','D':'DA','C':'CA', \
                            'E':'EA','F':'FA','G':'GA','H':'HA', \
                            'I':'IA','J':'JA'}
        
        self.assertEqual(expected_results,self.enums['student']['name2code'])

    
if __name__ == "__main__":
    suite = unittest.TestSuite()

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_With_Headers))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_UI))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_GetEnums))

    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 


